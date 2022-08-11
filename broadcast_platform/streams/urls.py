from django.urls import path
from . import views
app_name='streams'

urlpatterns = [
    path('upload/', views.StreamUploadView.as_view(), name='stream_upload'),
    path('list/', views.StreamListView, name='stream_list'),
    path('update/<int:pk>/', views.StreamUpdateView.as_view(), name='stream_update'),
    path('delete/<int:pk>/', views.StreamDeleteView, name='stream_delete'),

    path('streaming_now/', views.StreamingNowList.as_view(), name='streaming_now'),
    path('streaming_live/', views.StreamingLiveList.as_view(), name='streaming_live'),
    path('stream/<int:pk>/', views.StreamItem.as_view(), name='stream_item'),

    path('comment/', views.CreateComment, name='create_comment'),
    path('comment/list/', views.CommentList.as_view(), name='comment_list'),
    path('comment/blacklist/', views.BlackListComment, name='blacklist_comment'),
    path('cheers/', views.CheersStream, name='cheers_stream'),

    
    path('feedback/<int:pk>/', views.CreateFeedback.as_view(), name='create_feedback'),
    path('feedback/list/', views.ListFeedback.as_view(), name='list_feedback'),
]