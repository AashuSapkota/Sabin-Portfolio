from django.db import models
import datetime

class CostCenterModel(models.Model):
    costcenter_name = models.CharField(max_length=100, null=False, blank=False)
    costcenter_description = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)


class ItemCategoriesModel(models.Model):
    category_name = models.CharField(max_length=100, null=False, blank=False)
    category_description = models.TextField(null=True, blank=True)
    category_image = models.ImageField(upload_to='itemscategory_image',null=True)
    created_by = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)


class ItemsModel(models.Model):
    item_name = models.CharField(max_length=100, null=False)
    item_description = models.TextField(null=True, blank=True)
    item_image = models.ImageField(upload_to='items_image', null=True)
    item_rate = models.IntegerField(null=False, blank=False)
    item_category = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)


class TableModel(models.Model):
    table_name = models.CharField(max_length=100, null=False)
    table_code = models.CharField(max_length=100, null=True, blank=True)
    is_occupied = models.BooleanField(default=False, null=False, blank=False)
    created_by = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)
