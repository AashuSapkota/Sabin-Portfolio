import django_filters
from .models import User, UserRoleModel

class UserRoleFilter(django_filters.FilterSet):
    role_name = django_filters.CharFilter(field_name='role_name', lookup_expr='icontains')
    class Meta:
        model = UserRoleModel
        fields = ['role_description']


class UserFilter(django_filters.FilterSet):
    user_email = django_filters.CharFilter(field_name='user_email', lookup_expr = 'icontains')
    user_fullname = django_filters.CharFilter(field_name='user_fullname', lookup_expr = 'icontains')
    class Meta:
        model = User
        fields = ['user_fullname']