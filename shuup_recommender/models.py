# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import deletion
from django.utils.translation import ugettext_lazy as _


class ProductView(models.Model):
    product = models.ForeignKey(
        "shuup.Product",
        on_delete=deletion.CASCADE,
        related_name="user_views",
        verbose_name=_("product")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=deletion.CASCADE,
        related_name="product_views",
        verbose_name=_("user"),
        null=True, blank=True
    )
    created_on = models.DateTimeField(verbose_name=_("created on"), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("Product User View")
        verbose_name_plural = _("Product User Views")
