from rest_framework import serializers
from .models import *
from users.models import User


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenterModel
        fields = ['pk', 'costcenter_name', 'costcenter_description', 'created_on', 'created_by', 'is_deleted']
    
    def to_representation(self, instance):  
        ret = super().to_representation(instance)

        user_id = User.objects.get(pk=int(ret['created_by']))
        user_fullname = user_id.user_fullname
        ret['user_fullname'] = user_fullname
        return ret


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategoriesModel
        fields = ['pk', 'category_name', 'category_description', 'category_image', 'created_on', 'created_by', 'is_deleted']
    
    def to_representation(self, instance):  
        ret = super().to_representation(instance)
        user_id = User.objects.get(pk=int(ret['created_by']))
        user_fullname = user_id.user_fullname
        ret['user_fullname'] = user_fullname
        return ret


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsModel
        fields = ['pk', 'item_name', 'item_description', 'item_image', 'item_rate', 'item_category', 'created_on', 'created_by', 'is_deleted']
    def to_representation(self, instance):  
        ret = super().to_representation(instance)
        
        user_id = User.objects.get(pk=int(ret['created_by']))
        user_fullname = user_id.user_fullname
        ret['user_fullname'] = user_fullname

        item_category_id = ItemCategoriesModel.objects.get(pk=int(ret['item_category']))
        category_name = item_category_id.category_name
        ret['category_name'] = category_name

        return ret  


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableModel
        fields = ['pk', 'table_name', 'table_code', 'created_on', 'created_by', 'is_deleted']
    
    def to_representation(self, instance):  
        ret = super().to_representation(instance)

        user_id = User.objects.get(pk=int(ret['created_by']))
        user_fullname = user_id.user_fullname
        ret['user_fullname'] = user_fullname
        return ret

