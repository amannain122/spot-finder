from django.urls import path
from .views import PostList, PostDetail, UserView, TokenObtainView, ParkingStatusView, ParkingLotView

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('parking-status/', ParkingStatusView.as_view(), name='parking_status'),
    path('parkinglots/<str:parking_lot_id>/',
         ParkingLotView.as_view(), name='parkinglot-detail'),

]
