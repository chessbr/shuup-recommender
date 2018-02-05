# -*- coding: utf-8 -*-
import pytest
from shuup.core.models import Order, OrderStatus
from shuup.testing import factories

from shuup_recommender.models import ProductView
from shuup_recommender.recommenders import (
    EVERYTHING, MostSoldProducts, MostViewedProducts, PopularProducts
)


@pytest.mark.django_db
def test_most_sold_items():
    shop1 = factories.get_shop(identifier="shop1")
    shop2 = factories.get_shop(identifier="shop2")

    supplier = factories.get_default_supplier()

    # create products for shop1
    product1 = factories.create_product("p1", shop1, supplier)
    product2 = factories.create_product("p2", shop1, supplier)
    product3 = factories.create_product("p3", shop1, supplier)

    # create products for shop2
    product4 = factories.create_product("p4", shop2, supplier)
    product5 = factories.create_product("p5", shop2, supplier)

    # create orders for shop1
    # the most sold should be product3 (for this shop)
    factories.create_order_with_product(product1, supplier, 10, 1, shop=shop1)
    factories.create_order_with_product(product2, supplier, 20, 1, shop=shop1)
    factories.create_order_with_product(product3, supplier, 30, 1, shop=shop1)

    # create orders for shop2
    # the most sold should be product4 (for this shop)
    factories.create_order_with_product(product4, supplier, 100, 1, shop=shop2)
    factories.create_order_with_product(product5, supplier, 2, 1, shop=shop2)

    # set all orders completed
    Order.objects.all().update(status=OrderStatus.objects.get_default_complete())

    # get the most sold products for all shops
    # the rank should be: product4, product3, product2, product1, product5
    all_shops_most_sold = MostSoldProducts().recommend(EVERYTHING)
    product_ids = list(all_shops_most_sold["sold_rank"].keys())
    assert product_ids == [product4.id, product3.id, product2.id, product1.id, product5.id]

    # get the most sold products for all shop1
    # the rank should be: product3, product2, product1
    shop1_most_sold = MostSoldProducts(shop=shop1).recommend(EVERYTHING)
    product_ids = list(shop1_most_sold["sold_rank"].keys())
    assert product_ids == [product3.id, product2.id, product1.id]

    # get the most sold products for all shop2
    # the rank should be: product4, product5
    shop2_most_sold = MostSoldProducts(shop=shop2).recommend(EVERYTHING)
    product_ids = list(shop2_most_sold["sold_rank"].keys())
    assert product_ids == [product4.id, product5.id]


@pytest.mark.django_db
def test_most_viewed_items():
    shop = factories.get_default_shop()
    supplier = factories.get_default_supplier()

    product1 = factories.create_product("p1", shop, supplier)
    product2 = factories.create_product("p2", shop, supplier)
    product3 = factories.create_product("p3", shop, supplier)

    # views for product 1
    for i in range(10):
        ProductView.objects.create(product=product1)
    # views for product 2
    for i in range(20):
        ProductView.objects.create(product=product2)
    # views for product 3
    for i in range(15):
        ProductView.objects.create(product=product3)

    # get the most viewed products
    most_viewed = MostViewedProducts().recommend(EVERYTHING)
    product_ids = list(most_viewed["view_rank"].keys())
    assert product_ids == [product2.id, product3.id, product1.id]


@pytest.mark.django_db
def test_popular_items():
    shop1 = factories.get_shop(identifier="shop1")
    shop2 = factories.get_shop(identifier="shop2")

    supplier = factories.get_default_supplier()

    # create products for shop1
    product1 = factories.create_product("p1", shop1, supplier)
    product2 = factories.create_product("p2", shop1, supplier)
    product3 = factories.create_product("p3", shop1, supplier)

    # create products for shop2
    product4 = factories.create_product("p4", shop2, supplier)
    product5 = factories.create_product("p5", shop2, supplier)

    # create orders for shop1
    # the most sold should be product3 (for this shop)
    factories.create_order_with_product(product1, supplier, 10, 1, shop=shop1)
    factories.create_order_with_product(product2, supplier, 20, 1, shop=shop1)
    factories.create_order_with_product(product3, supplier, 30, 1, shop=shop1)

    # create orders for shop2
    # the most sold should be product4 (for this shop)
    factories.create_order_with_product(product4, supplier, 100, 1, shop=shop2)
    factories.create_order_with_product(product5, supplier, 2, 1, shop=shop2)

    # set all orders completed
    Order.objects.all().update(status=OrderStatus.objects.get_default_complete())

    # views for product 1
    for i in range(10):
        ProductView.objects.create(product=product1)
    # views for product 2
    for i in range(20):
        ProductView.objects.create(product=product2)
    # views for product 3
    for i in range(40):
        ProductView.objects.create(product=product3)
    # views for product 4
    for i in range(10):
        ProductView.objects.create(product=product4)
    # views for product 5
    for i in range(20):
        ProductView.objects.create(product=product5)

    # get the most viewed products
    popular = PopularProducts().recommend(EVERYTHING)
    product_ids = list(popular["rank"].keys())
    assert product_ids == [product3.id, product4.id, product2.id, product5.id, product1.id]
