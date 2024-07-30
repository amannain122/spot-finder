from django.urls import path
<<<<<<< HEAD
from .views import UserView, TokenObtainView, ParkingListView, ParkingLotView, BookingViewSet, CancelBookingView, DeleteBookingView, BookingAPI
=======
from .views import PostList, PostDetail, UserView, TokenObtainView, ParkingStatusView, ParkingLotView, BookingViewSet
from .views import PostList, PostDetail, UserView, TokenObtainView, ParkingStatusView, ParkingLotView, BookingViewSet, CancelBookingView, DeleteBookingView
>>>>>>> 261ed3d (fixed minor error)

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('parking-list/', ParkingListView.as_view(), name='parking_list'),
    path('parking-status/<str:parking_lot_id>/',
         ParkingLotView.as_view(), name='parking-lot-detail'),
    path('bookings/', BookingViewSet.as_view(), name='booking'),
    path('all-bookings/', BookingAPI.as_view(), name='all_booking'),
    path('bookings/<int:pk>/cancel/',
         CancelBookingView.as_view(), name='cancel-booking'),
    path('bookings/<int:pk>/delete/',
         DeleteBookingView.as_view(), name='delete-booking')
]
