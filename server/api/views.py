from django.db import connection
from django.http import JsonResponse
from .serializers import UserSerializer, MyTokenObtaionPairSerializer, PostSerializer, ParkingStatusSerializer
import os
import pandas as pd
from rest_framework import generics
from api.models import Post
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PostSerializer
from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtaionPairSerializer, PostSerializer
from .s3_utiils import upload_file_to_s3, download_csv_from_s3
from django.shortcuts import render
from django.views import View
from .athena_utils import execute_athena_query, get_query_results
import boto3  # Make sure boto3 is imported
from botocore.exceptions import ClientError

from .models import User
AWS_S3_REGION_NAME = 'us-east-1'


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
                    file_url = upload_file_to_s3(file)
                    # Optionally, you can save the S3 file URL to your user object
                    # user.file_url = file_url
                    # user.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            return Response({"detail": "Error creating user", "error": str(exe)}, status=status.HTTP_400_BAD_REQUEST)


class CSVDataView(APIView):
    def get(self, request):
        s3_key = 'SampleAthena/sample.csv'
        data = download_csv_from_s3(s3_key)
        if data is not None:
            return JsonResponse({'data': data.to_dict(orient='records')})
        else:
            return JsonResponse({'error': 'Failed to fetch data from S3'}, status=500)


class AthenaQueryView(View):
    template_name = 'athena_results.html'
    query = "SELECT * FROM sample_db.sampletable LIMIT 10;"
    database = "sample_db"
    output_location = "s3://spotfinder-data-bucket/Athena_output/"

    def get(self, request):
        try:
            query_execution_id = execute_athena_query(
                self.query, self.database, self.output_location)
            results_df = get_query_results(query_execution_id)
            results = results_df.to_html()
        except Exception as e:
            results = str(e)

        return render(request, self.template_name, {'results': results})

    def check_query_status(query_execution_id):
        athena_client = boto3.client('athena', region_name=AWS_S3_REGION_NAME)
        max_attempts = 5  # Adjust this as needed
        retry_delay = 2  # Seconds between retries

        for attempt in range(max_attempts):
            try:
                response = athena_client.get_query_execution(
                    QueryExecutionId=query_execution_id)
                query_status = response['QueryExecution']['Status']['State']
                return query_status
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidRequestException':
                    if attempt < max_attempts - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return None  # Or handle the error appropriately
                else:
                    return None  # Or handle the error appropriately

        return None  # Fallback if all retries fail


def list_redshift_tables(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              AND table_schema NOT IN ('information_schema', 'pg_catalog')
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
    return JsonResponse(data, safe=False)


class ParkingStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        file_path = os.path.join(
            settings.BASE_DIR, 'data/parking_status.csv')
        parking_data = pd.read_csv(file_path)

        # Get the latest data (assuming the CSV is sorted by Timestamp)
        latest_data = parking_data.iloc[-1]

        total_spots = len(latest_data) - 1
        available_spots = (latest_data == 'empty').sum()
        reserved_spots = (latest_data == 'occupied').sum()

        # Prepare the spots data
        spots = [
            {'spot': spot, 'status': latest_data[spot]}
            for spot in latest_data.index if spot != 'Timestamp'
        ]

        # Prepare the response data
        response_data = {
            "id": 1,
            'coordinates': {"latitude": 43.7760345, "longitude": -79.2601504},
            'total_spots': total_spots,
            'available_spots': available_spots,
            'reserved_spots': reserved_spots,
            'spots': spots,
        }

        serializer = ParkingStatusSerializer(response_data)

        return Response(serializer.data)
