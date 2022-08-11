from rest_framework import serializers
from .models import *


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleModel
        fields = ['pk', 'role_name', 'role_description', 'created_on', 'created_by', 'is_deleted']
    
    def to_representation(self, instance):  
        ret = super().to_representation(instance)

        user_id = User.objects.get(pk=int(ret['created_by']))
        user_fullname = user_id.user_fullname
        ret['user_fullname'] = user_fullname
        return ret

        


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'user_email', 'user_fullname', 'user_role', 'created_by', 'created_on', 'is_deleted']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        print('here')

        user_id = User.objects.get(pk=ret['created_by'])
        user_created_by = user_id.user_fullname
        ret['user_created_by'] = user_created_by

        if ret['user_role'] == '0':
            ret['teller_role'] = '0'
            return ret
        else: 
            role_id = UserRoleModel.objects.get(pk=ret['user_role'])
            role_name = role_id.role_name
            ret['teller_role'] = role_name
            return ret

