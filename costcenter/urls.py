from django.urls import path
from .import views

app_name = 'costcenter'
urlpatterns = [
    # urls for costcenter
    path('create/costcenter/', views.CreateCostCenterAPI.as_view(), name='create_costcenter'),
    path('list/costcenter/', views.ListCostCenterAPI.as_view(), name='list_costcenter'),
    path('update/costcenter/<int:pk>/', views.UpdateCostCenterAPI.as_view(), name='update_costcenter'),
    path('delete/costcenter/<int:pk>/', views.DeleteCostCenterAPI.as_view(), name='delete_costcenter'),

    # urls for itemcategories
    path('create/itemcategory/', views.CreateItemCategoryAPI.as_view(), name='create_itemcategory'),
    path('list/itemcategory/', views.ListItemCategoryAPI.as_view(), name='list_itemcategory'),
    path('update/itemcategory/<int:pk>/', views.UpdateItemCategoryAPI.as_view(), name='update_itemcategory'),
    path('delete/itemcategory/<int:pk>/', views.DeleteItemCategoryAPI.as_view(), name='delete_itemcategory'),

    # urls for items
    path('create/item/', views.CreateItemAPI.as_view(), name='create_item'),
    path('list/item/', views.ListItemAPI.as_view(), name='list_item'),
    path('update/item/<int:pk>/', views.UpdateItemAPI.as_view(), name='update_item'),
    path('delete/item/<int:pk>/', views.DeleteItemAPI.as_view(), name='delete_item'),

    # urls for table
    path('create/table/', views.CreatetableAPI.as_view(), name='create_table'),
    path('list/table/', views.ListTableAPI.as_view(), name='list_table'),
    path('update/table/<int:pk>/', views.UpdateTableAPI.as_view(), name='update_table'),
    path('delete/table/<int:pk>/', views.DeleteTableAPI.as_view(), name='delete_table'),

]