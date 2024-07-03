from django.urls import path
from .views import PostList, PostDetail, UserView, TokenObtainView, list_redshift_tables, ParkingStatusView

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('list_redshift_tables/', list_redshift_tables,
         name='list_redshift_tables'),
    path('parking-status/', ParkingStatusView.as_view(), name='parking_status'),
]
