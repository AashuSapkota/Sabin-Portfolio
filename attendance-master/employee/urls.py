from os import name
from django.urls import path
from . import views

app_name= 'employee'
urlpatterns = [
    path('', views.EmployeeListView, name='employee_list'),
    path('register/', views.EmployeeRegisterView.as_view(), name='employee_register'),
    path('identification/', views.EmployeeIdentificationView.as_view(), name='employee_identification'),
    path('camera/', views.EmployeeCameraView.as_view(), name='employee_camera'),
    path('details/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('delete/<int:pk>', views.EmployeeDeleteView, name='employee_delete'),
    path('fetch_profile/',views.FetchProfile,name="employee_fetch"),
    # path('log/',views.EmployeeLogView.as_view(),name="employee_log"),
    path('log/', views.EmployeeLogEntryView, name='employee_log')
]