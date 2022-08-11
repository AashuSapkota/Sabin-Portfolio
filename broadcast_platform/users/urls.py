from django.urls import include, path
from . import views

app_name= 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('list/', views.UserListView, name='user_list'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', views.UserDeleteView, name='user_delete'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('profile/change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='user_change_password'),

    path('password_reset_request/', views.password_reset_request, name='password_change_request'),
    path('password_request_changed/', views.password_reset, name='password_request_changed'),

    
    path('admin/create/', views.AdminCreateView.as_view(), name='admin_create'),
    path('admin/list/', views.AdminListView, name='admin_list'),
    path('admin/update/<int:pk>', views.AdminUpdateView.as_view(), name='admin_update'),

    
    path('blocked/list/', views.BlockedUsersList.as_view(), name='blocked_user_list'),
    path('block/<int:pk>/', views.BlockUser.as_view(), name='block_user'),
    path('unblock/<int:pk>/', views.UnBlockUser.as_view(), name='unblock_user'),


    
    path('contact_admin/', views.ContactAdmin.as_view(), name='contact_admin'),
    # path('add_country/', views.CountryData.as_view(), name='country_data'),
]