
from rest_framework import generics
from api.models import Post
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtaionPairSerializer, PostSerializer, ParkingLotSerializer
from .utils import METADATA, query_athena, get_query_results, results_to_dataframe
from .models import User


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
        # access_token = serializer.validated_data['access']
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


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    pass


class UserView(APIView):
    permission_classes = [IsAdminOrUserPermission]

    def post(self, request, format='json'):
        try:
            serializer = UserSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                # Save user data
                user = serializer.save()

                # Handle file upload to S3 if applicable
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    # file_url = upload_file_to_s3(file)
                    # Optionally, you can save the S3 file URL to your user object
                    # user.file_url = file_url
                    # user.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            return Response({"detail": "Error creating user", "error": str(exe)}, status=status.HTTP_400_BAD_REQUEST)


def merge_data(metadata, spots):
    parking_lots = []
    for idx, lot in enumerate(metadata):
        lot_spots = [spot for spot in spots if spot["ParkingLotID"]
                     == lot["ParkingLotID"]]
        spots_list = [{"spot": f"SP{i}", "status": lot_spots[0].get(
            f"SP{i}", "empty")} for i in range(1, 24)]
        coordinates = {"latitude": 0.0, "longitude": 0.0}
        if lot["Location"]:
            lat, lon = map(float, lot["Location"].split(","))
            coordinates = {"latitude": lat, "longitude": lon}
        total_spots = lot["Number of Spots"]
        available_spots = sum(
            1 for spot in spots_list if spot["status"] == "empty")
        reserved_spots = total_spots - available_spots
        parking_lots.append({
            "id": idx + 1,
            "parking_id": lot["ParkingLotID"],
            "coordinates": coordinates,
            "total_spots": total_spots,
            "available_spots": available_spots,
            "reserved_spots": reserved_spots,
            "address": lot["Address"],
            "image": lot["URL"],
            "spots": spots_list
        })
    return parking_lots


class ParkingStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = "SELECT * FROM athena_spot_finder.parking_lots;"
        database = "sample_db"
        output_location = "s3://spotfinder-data-bucket/Athena_output/"
        query_execution_id = query_athena(query, database, output_location)
        results = get_query_results(query_execution_id)

        spots_data = results_to_dataframe(results)
        data = merge_data(METADATA, spots_data)
        serializer = ParkingLotSerializer(data, many=True)
        return Response(serializer.data)


class ParkingLotView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, parking_lot_id=None):
        query = "SELECT * FROM athena_spot_finder.parking_lots;"
        database = "sample_db"
        output_location = "s3://spotfinder-data-bucket/Athena_output/"
        query_execution_id = query_athena(query, database, output_location)
        results = get_query_results(query_execution_id)
        spots_data = results_to_dataframe(results)

        data = merge_data(METADATA, spots_data)
        if parking_lot_id:
            parking_lot = next(
                (lot for lot in data if lot["parking_id"] == parking_lot_id), None)
            if parking_lot:
                serializer = ParkingLotSerializer(parking_lot)
                return Response(serializer.data)
            else:
                return Response({"error": "Parking lot not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ParkingLotSerializer(data, many=True)
            return Response(serializer.data)
