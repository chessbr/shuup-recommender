# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from django.db.models import Q
from django_pandas.io import read_frame
from shuup.core.models import OrderLine, OrderStatus

from shuup_recommender.models import ProductView

from ._base import BaseRecommender
from ._consts import EVERYTHING


def distance(x, y):
    return np.sqrt(np.power(x, 2) + np.power(y, 2))


class MostSoldProducts(BaseRecommender):
    """ Most sold products recommender

    Recommend the most sold products

    To filter orders or shops, use the kwargs param when
    instantiating the recommender:

    kwargs:
        base_orders (queryset of shuup.Order): calculates the most
        sold products from this queryset.

        shop (shuup.Shop): filters orders based on this shop.

        shops (iterator[shuup.Shop]): filters orders based on these shops.

    Usage example:
        ```
        most_sold_products = MostSoldProducts(shop=my_shop).recommend(20)
        ```
    """

    def _get_order_lines(self):
        orders = self.kwargs.get("base_orders")

        if orders:
            order_lines = OrderLine.objects.filter(order__in=orders).products()
        else:
            filters = Q(order__status=OrderStatus.objects.get_default_complete())

            shop = self.kwargs.get("shop")
            shops = self.kwargs.get("shops")
            if shop:
                filters &= Q(order__shop=shop)
            elif shops:
                filters &= Q(order__shop__in=shops)

            order_lines = OrderLine.objects.products().filter(filters)
        return order_lines

    def recommend(self, n=10, **kwargs):
        """
        :returns: DataFrame of [product_id, rank] sorted by rank DESC
            product_id (int): ID of the product
            sold_rank (float): rank of the product (from 0 to 1)
        """
        order_lines = self._get_order_lines()

        # read order lines into DataFrame
        items_df = read_frame(order_lines, fieldnames=["product_id", "quantity"], verbose=False)

        # group by product ID and sum quantities
        sold_items = items_df.groupby(["product_id"]).sum()

        # get the max value of quantity
        max_value = sold_items["quantity"].max()

        # normalize the values
        sold_items["sold_rank"] = (sold_items["quantity"] / max_value).apply(pd.to_numeric)

        # sort the products and remove auxiliar columns
        ranked_products = sold_items[["sold_rank"]].sort_values("sold_rank", ascending=False)

        # if `n` is 0 or None, return everything
        return ranked_products.head(n) if n else ranked_products


class MostViewedProducts(BaseRecommender):
    """ Most viwed products recommender

    Recommend the most viwed products

    This recommender works by using then
    shuup_recommender.ProductView model instances.

    Thus, it is your responsability to create instances
    of that model everytime one actually view the product.

    All ProductView will be used by this recommender by defaut.
    To use a custom set of views, you should use the
    `views` kwargs key when instantiating the recommender:

        ```
        most_viewed_products = MostViewedProducts(
            views=ProductView.objects.filter(user__isnull=True)
        ).recommend()
        ```
    """

    def _get_views(self):
        if self.kwargs.get("views"):
            return self.kwargs["views"]
        return ProductView.objects.all()

    def recommend(self, n=10, **kwargs):
        """
        :returns: DataFrame of [product_id, rank] sorted by rank DESC
            product_id (int): ID of the product
            view_rank (float): rank of the product (from 0 to 1)
        """
        product_views_df = read_frame(self._get_views(), fieldnames=["product_id"], verbose=False)
        product_views_df["views"] = 1

        # group by product ID and sum views
        viewed_products = product_views_df.groupby(["product_id"]).sum()

        # get the max value of views
        max_value = viewed_products["views"].max()

        # normalize the values - this way we can easily plot them later
        viewed_products["view_rank"] = (viewed_products["views"] / max_value).apply(pd.to_numeric)

        # sort the products and remove auxiliar columns
        ranked_products = viewed_products[["view_rank"]].sort_values("view_rank", ascending=False)

        # if `n` is 0 or None, return everything
        return ranked_products.head(n) if n else ranked_products


class PopularProducts(object):
    """Popular products recommender

    Recommend the popular products

    This is the mix of most sold and most viewed products recommenders.

    All kwargs parameters from `MostViewedProducts` and `MostSoldProducts`
    can be used.
    """

    def recommend(self, n=10, **kwargs):
        """
        :returns: DataFrame of [product_id, rank] sorted by rank DESC
            product_id (int): ID of the product
            rank (float): rank of the product (from 0 to 1)
        """
        viewed_products_rank = MostViewedProducts(**kwargs).recommend(EVERYTHING)
        sold_items_rank = MostSoldProducts(**kwargs).recommend(EVERYTHING)

        products_rank = pd.merge(sold_items_rank, viewed_products_rank, how="outer", left_index=True, right_index=True)

        # calcule the Pythagorean distance
        products_rank["rank"] = distance(products_rank["view_rank"], products_rank["sold_rank"])

        # normalize data
        max_value = products_rank["rank"].max()
        products_rank["rank"] = products_rank["rank"] / max_value

        # sort values and remove auxiliar columns
        popular_products = products_rank[["rank"]].sort_values("rank", ascending=False)

        # if `n` is 0 or None, return everything
        return popular_products.head(n) if n else popular_products
