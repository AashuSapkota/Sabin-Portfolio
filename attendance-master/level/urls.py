from django.urls import path
from . import views

app_name = 'level'
urlpatterns = [
    path('', views.LevelListView, name='level_list'),
    path('create/', views.LevelCreateView.as_view(), name='level_create'),
    path('update/<int:pk>/', views.LevelUpdateView.as_view(), name='level_update'),
    path('delete/<int:pk>/', views.LevelDeleteView, name='level_delete'),
]