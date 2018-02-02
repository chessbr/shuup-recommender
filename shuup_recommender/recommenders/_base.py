# -*- coding: utf-8 -*-
import pandas as pd


class BaseRecommender(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def recommend(self, n=10, **kwargs):
        """ Recommend items
        :param n int: number of items to recommend. Default 10.
        If zero or None, all items will be returned.

        :rtype pandas.DataFrame
        :returns: DataFrame with recommendations
        """
        return pd.DataFrame()
