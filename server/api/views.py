
from asgiref.sync import async_to_sync
from django.conf import settings
from django.middleware.csrf import get_token
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import status
from cryptography.fernet import Fernet, InvalidToken
from .serializers import UserSerializer, MyTokenObtaionPairSerializer, BookingSerializer, ParkingLotSerializer, AllBookingSerializer
from .utils import METADATA, query_athena, get_query_results, results_to_dataframe, merge_data
from .models import User, Booking
from rest_framework.views import APIView
from .serializers import ParkingLotSerializer
import core.settings as set
import environ

env = environ.Env()


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


class ParkingListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cache_key = 'parking_lots_data'

        cached_data = cache.get(cache_key)

        if cached_data:
            # Update spot status from cache before returning it
            self.update_spot_status(cached_data)
            cache.set(cache_key, cached_data, timeout=3600)
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
        self.update_spot_status(data)

        serializer = ParkingLotSerializer(data, many=True)

        cache.set(cache_key, serializer.data, timeout=3600)

        return Response(serializer.data)

    def update_spot_status(self, data):
        for lot in data:
            parking_id = lot['parking_id']
            available_spots_count = lot.get('available_spots', 0)
            reserved_spots_count = lot.get('reserved_spots', 0)

            for spot in lot['spots']:
                spot_id = spot['spot']
                booking = Booking.objects.filter(
                    parking_id=parking_id, parking_spot=spot_id, booking_status="booked").first()

                if booking and spot['status'] == 'empty':
                    spot['status'] = 'occupied'
                    available_spots_count -= 1
                    reserved_spots_count += 1

            lot['available_spots'] = available_spots_count
            lot['reserved_spots'] = reserved_spots_count


class ParkingLotView(APIView):
    permission_classes = [permissions.AllowAny]
    PARKING_LOT_CHOICES = ['PL01', 'PL02', 'PL03']

    def get(self, request, parking_lot_id=None):
        cache_key = 'parking_status_lots_data'
        cached_data = cache.get(cache_key)

        if parking_lot_id and parking_lot_id.upper() not in self.PARKING_LOT_CHOICES:
            return Response({"error": "Parking Detail Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        if cached_data:
            if parking_lot_id:
                parking_lot = next(
                    (lot for lot in cached_data if lot["parking_id"] == parking_lot_id.upper()), None)
                if parking_lot:
                    self.update_spot_status(parking_lot)
                    cache.set(cache_key, cached_data, timeout=3600)
                    serializer = ParkingLotSerializer(parking_lot)
                    return Response(serializer.data)
                else:
                    return Response({"error": "Parking lot not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                for lot in cached_data:
                    self.update_spot_status(lot)
                cache.set(cache_key, cached_data, timeout=3600)
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
                self.update_spot_status(parking_lot)
                serializer = ParkingLotSerializer(parking_lot)
                cache.set(cache_key, data, timeout=3600)
                return Response(serializer.data)
            else:
                return Response({"error": "Parking lot not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            for lot in data:
                self.update_spot_status(lot)
            serializer = ParkingLotSerializer(data, many=True)
            cache.set(cache_key, data, timeout=3600)
            return Response(serializer.data)

    def update_spot_status(self, parking_lot):
        parking_id = parking_lot['parking_id']
        initial_available_spots = parking_lot.get('available_spots', 0)
        initial_reserved_spots = parking_lot.get('reserved_spots', 0)

        for spot in parking_lot['spots']:
            spot_id = spot['spot']
            # Checking if there's a 'booked' status or 'canceled' status for this parking lot and spot
            booking = Booking.objects.filter(
                parking_id=parking_id, parking_spot=spot_id).order_by('-updated_at').first()

            if booking:
                if booking.booking_status == "booked":
                    if spot['status'] == 'empty':
                        spot['status'] = 'occupied'
                        initial_available_spots -= 1
                        initial_reserved_spots += 1
                elif booking.booking_status == "canceled":
                    if spot['status'] == 'occupied':
                        spot['status'] = 'empty'
                        initial_reserved_spots -= 1
                        initial_available_spots += 1

                # Update the parking lot's available_spots and reserved_spots counts
        parking_lot['available_spots'] = initial_available_spots
        parking_lot['reserved_spots'] = initial_reserved_spots


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
            # Check if the user has already booked the spot
            if Booking.objects.filter(user=request.user, booking_status='booked').exists():
                return Response({"detail": "You have already booked a parking spot."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the parking spot is already booked
            parking_spot = request.data.get('parking_spot')
            parking_id = request.data.get('parking_id')

            if Booking.objects.filter(parking_spot=parking_spot, parking_id=parking_id, booking_status='booked').exists():
                return Response({"detail": "This parking spot is already booked. Please choose another spot."}, status=status.HTTP_400_BAD_REQUEST)

            note = serializer.save()
            if note:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def decode_token(token):
    key = bytes(env("CRYPTO_KEY"), 'utf-8')
    fernet = Fernet(key)

    try:
        decoded = fernet.decrypt(bytes(token, 'utf-8'))
        return decoded.decode()
    except InvalidToken:
        return None


class BookingAPI(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = AllBookingSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return Response({"error": "Token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        decoded_token = decode_token(token)

        if not decoded_token:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # If token is valid, proceed with the usual response
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
