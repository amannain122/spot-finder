from django.urls import path
from .views import PostList, PostDetail, UserView, TokenObtainView, ParkingStatusView, ParkingLotView, BookingViewSet
from .views import PostList, PostDetail, UserView, TokenObtainView, ParkingStatusView, ParkingLotView, BookingViewSet, CancelBookingView, DeleteBookingView

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('parking-status/', ParkingStatusView.as_view(), name='parking_status'),
    path('parkinglots/<str:parking_lot_id>/',
         ParkingLotView.as_view(), name='parkinglot-detail'),
    path('bookings/', BookingViewSet.as_view(), name='booking'),
    path('bookings/<int:pk>/cancel/',
         CancelBookingView.as_view(), name='cancel-booking'),
    path('bookings/<int:pk>/delete/',
         DeleteBookingView.as_view(), name='delete-booking')
]
