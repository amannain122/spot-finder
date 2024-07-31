
from asgiref.sync import async_to_sync
from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import status
from .serializers import UserSerializer, MyTokenObtaionPairSerializer, BookingSerializer, ParkingLotSerializer, AllBookingSerializer
from .utils import METADATA, query_athena, get_query_results, results_to_dataframe, merge_data
from .models import User, Booking
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ParkingLotSerializer
from django.core.cache import cache


class IsAdminOrUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        if request.user.is_authenticated and (request.user.user_type == 0 or request.user.user_type == 1):
            if request.method == 'POST' and request.user.user_type != 0:
                return False
            else:
                return True
        return False


class TokenObtainView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtaionPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        refresh_token = serializer.validated_data['refresh']
        access_token = serializer.validated_data['access']
        get_token(request)
        res.set_cookie("refresh_token", refresh_token, max_age=settings.SIMPLE_JWT.get(
            'REFRESH_TOKEN_LIFETIME').total_seconds(), samesite='Lax', secure=False, httponly=True)
        res.data.pop('refresh')
        return res


class UserView(APIView):
    permission_classes = [IsAdminOrUserPermission]

    def get(self, request):
        try:
            user = request.user
            instance = User.objects.get(id=user.pk)
            if instance:
                serializer = UserSerializer(
                    instance, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format='json'):
        try:
            serializer = UserSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            return Response({"detail": "Error creating user", "error": str(exe)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ParkingListView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         query = "SELECT * FROM athena_spot_finder.parking_lots;"
#         database = "sample_db"
#         output_location = "s3://spotfinder-data-bucket/Athena_output/"
#         query_execution_id = query_athena(query, database, output_location)
#         results = get_query_results(query_execution_id)

#         spots_data = results_to_dataframe(results)
#         data = merge_data(METADATA, spots_data)
#         serializer = ParkingLotSerializer(data, many=True)
#         return Response(serializer.data)


class ParkingListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cache_key = 'parking_lots_data'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Convert async function calls to sync using async_to_sync
        query = 'SELECT * FROM "AwsDataCatalog"."spotfinder-schema"."parking_list_lots"'
        database = 'spotfinder-schema'
        output_location = "s3://spotfinder-data-bucket/Athena_output/"

        query_execution_id = async_to_sync(query_athena)(
            query, database, output_location)
        results = async_to_sync(get_query_results)(query_execution_id)

        spots_data = results_to_dataframe(results)

        data = merge_data(METADATA, spots_data)
        serializer = ParkingLotSerializer(data, many=True)

        cache.set(cache_key, serializer.data, timeout=3600)

        return Response(serializer.data)


class ParkingLotView(APIView):
    permission_classes = [permissions.AllowAny]
    PARKING_LOT_CHOICES = ['PL01', 'PL02', 'PL03']

    def get(self, request, parking_lot_id=None):
        cache_key = 'parking_status_lots_data'

        if parking_lot_id and parking_lot_id.upper() not in self.PARKING_LOT_CHOICES:
            return Response({"error": "Parking Detail Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        cached_data = cache.get(cache_key)

        if cached_data:
            if parking_lot_id:
                parking_lot = next(
                    (lot for lot in cached_data if lot["parking_id"] == parking_lot_id.upper()), None)
                if parking_lot:
                    serializer = ParkingLotSerializer(parking_lot)
                    return Response(serializer.data)
                else:
                    return Response({"error": "Parking lot not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(cached_data)

        query = 'SELECT * FROM "AwsDataCatalog"."spotfinder-schema"."parking_list_lots"'
        database = 'spotfinder-schema'
        output_location = "s3://spotfinder-data-bucket/Athena_output/"
        query_execution_id = async_to_sync(query_athena)(
            query, database, output_location)
        results = async_to_sync(get_query_results)(query_execution_id)
        spots_data = results_to_dataframe(results)

        data = merge_data(METADATA, spots_data)
        if parking_lot_id:
            parking_lot = next(
                (lot for lot in data if lot["parking_id"] == parking_lot_id.upper()), None)
            if parking_lot:
                serializer = ParkingLotSerializer(parking_lot)
                cache.set(cache_key, data, timeout=3600)
                return Response(serializer.data)
            else:
                return Response({"error": "Parking lot not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ParkingLotSerializer(data, many=True)
            return Response(serializer.data)


class BookingViewSet(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.request.user.id
        return Booking.objects.filter(user=id)

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            note = serializer.save()
            if note:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingAPI(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = AllBookingSerializer


class CancelBookingView(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.booking_status != 'booked':
            return Response({'error': 'Booking can only be canceled if it is currently booked'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the status to 'canceled'
        instance.booking_status = 'canceled'
        instance.save()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteBookingView(DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.booking_status in ['canceled', 'expired']:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Only canceled or expired bookings can be deleted'}, status=status.HTTP_400_BAD_REQUEST)
