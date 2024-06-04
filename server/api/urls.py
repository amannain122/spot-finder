from django.urls import path
from .views import PostList, PostDetail, UserView, TokenObtainView

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
]
