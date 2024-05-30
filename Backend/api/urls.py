from django.urls import path
from .views import PostList, PostDetail

app_name = 'spotFinder'

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
]
