from django.urls import path
from . import views

app_name = 'position'
urlpatterns = [
    path('', views.PositionListView, name='position_list'),
    path('create/', views.PositionCreateView.as_view(), name='position_create'),
    path('update/<int:pk>/', views.PositionUpdateView.as_view(), name='position_update'),
    path('delete/<int:pk>/', views.PositionDeleteView, name='position_delete'),
]