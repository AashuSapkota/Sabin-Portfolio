from django.db import models
import datetime


class OrderModel(models.Model):
    table_id = models.CharField(max_length=100, null=False, blank=False)
    order_masterid = models.CharField(max_length=100, null=False, blank=False)


class OrderDetailModel(models.Model):
    order_masterid = models.CharField(max_length=100, null=False, blank=False)
    item_id = models.CharField(max_length=100, null=False, blank=False)
    item_quantity = models.IntegerField(null=False, blank=False)
    item_rate = models.IntegerField(null=False, blank=False)
    total_price = models.IntegerField(null=False, blank=False)

