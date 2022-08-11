import django_filters
from .models import CostCenterModel, ItemCategoriesModel, ItemsModel, TableModel

class CostCenterFilter(django_filters.FilterSet):
    costcenter_name = django_filters.CharFilter(field_name='costcenter_name', lookup_expr='icontains')
    class Meta:
        model = CostCenterModel
        fields = ['costcenter_description']


class ItemCategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name='category_name', lookup_expr='icontains')
    class Meta:
        model = ItemCategoriesModel
        fields = ['category_description']


class ItemFilter(django_filters.FilterSet):
    item_name = django_filters.CharFilter(field_name='item_name', lookup_expr='icontains')
    class Meta:
        model = ItemsModel
        fields = ['item_description']


class TableFilter(django_filters.FilterSet):
    table_name = django_filters.CharFilter(field_name='table_name', lookup_expr='icontains')
    class Meta:
        model = TableModel
        fields = ['table_code']