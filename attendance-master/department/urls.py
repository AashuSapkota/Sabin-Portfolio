from django.urls import path
from . import views


app_name = 'department'
urlpatterns = [
    path('', views.DepartmentListView, name='department_list'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('update/<int:pk>/', views.DepartmentUpdateView.as_view(),
         name='department_update'),
    path('delete/<int:pk>/', views.DepartmentDeleteView, name='department_delete'),
]
