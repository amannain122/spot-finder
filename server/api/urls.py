from django.urls import path
from .views import PostList, PostDetail, UserView, TokenObtainView, GenerateQRCodeAPIView, confirm_booking

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('generate-qr/', GenerateQRCodeAPIView.as_view(), name='generate-qr'),
    path('confirm-booking/', confirm_booking, name='confirm_booking'),
]
