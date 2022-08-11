from django.urls import include, path
from .import views


app_name = 'users'
urlpatterns = [
    path('loginapi/', views.UserLoginAPI.as_view(), name='user_login'),

    # urls for UserRoleModel
    path('create/userrole/', views.CreateUserRoleAPI.as_view(), name='create_user_role'),
    path('list/userrole/', views.ListUserRoleAPI.as_view(), name='list_user_role'),
    path('update/userrole/<int:pk>/', views.UpdateUserRoleAPI.as_view(), name='update_user_role'),
    path('delete/userrole/<int:pk>/', views.DeleteUserRoleAPI.as_view(), name='delete_user_role'),

    # urls for UserModel
    path('create/user/', views.UserCreateAPI.as_view(), name='create_user'),
    path('list/user/', views.UserListAPI.as_view(), name='list_user'),
    path('update/user/<int:pk>/', views.UserUpdateAPI.as_view(), name='update_user'),
    path('delete/user/<int:pk>/', views.UserDeleteAPI.as_view(), name='delete_user'),

    # urls for previlege
    path('userroleprevilege/updateroleprevilegeapi/<int:role_id>/',
         views.UpdateRolePrevilageAPI.as_view(), name='userroleprevilege_updateroleprevilege'),
    path('userroleprevilege/updateuserprevilegeapi/<int:user_id>/',
         views.UpdateUserPrevilageAPI.as_view(), name='userroleprevilege_updateuserprevilege'),

]