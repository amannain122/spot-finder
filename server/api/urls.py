from django.urls import path
<<<<<<< HEAD
from .views import PostList, PostDetail, UserView, TokenObtainView
=======
from .views import PostList, PostDetail, UserView, TokenObtainView,CSVDataView,AthenaQueryView
>>>>>>> ca96889 (code changes for Athena conection)

app_name = 'spotFinder'

urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('login/', TokenObtainView.as_view(), name='login'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
<<<<<<< HEAD
=======
    path('csv-data/', CSVDataView.as_view(), name='csv_data'),
    path('athena/', AthenaQueryView.as_view(), name='athena_query'),
    path('status/', AthenaQueryView.check_query_status, name='check_query_status'),
>>>>>>> ca96889 (code changes for Athena conection)
]
