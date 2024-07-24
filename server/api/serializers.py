from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, User, Booking


class MyTokenObtaionPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtaionPairSerializer, cls).get_token(user)

        token['user_id'] = user.id
        token['user_type'] = user.user_type
        token['email'] = user.email

        return token


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'password', 'avatar', 'is_active', 'email_verified', 'last_login']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {
            'write_only': True}, 'email_verified': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type',
                  'car_no_plate', 'is_active', 'email_verified', 'created_at', "updated_at"]
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {
            'write_only': True}, 'email_verified': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if ('password' in [x for x in validated_data]):
            validated_data.pop('password')
        return super().update(instance, validated_data)


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ParkingStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    coordinates = CoordinatesSerializer()
    total_spots = serializers.IntegerField()
    available_spots = serializers.IntegerField()
    reserved_spots = serializers.IntegerField()
    spots = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


class ParkingSpotSerializer(serializers.Serializer):
    spot = serializers.CharField(max_length=10)
    status = serializers.CharField(max_length=10)


class ParkingLotSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parking_id = serializers.CharField(max_length=10)
    coordinates = serializers.DictField()
    total_spots = serializers.IntegerField()
    available_spots = serializers.IntegerField()
    reserved_spots = serializers.IntegerField()
    address = serializers.CharField(max_length=200)
    image = serializers.URLField()
    spots = ParkingSpotSerializer(many=True)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'parking_id', 'parking_spot', 'parking_charge',
            'parking_time', 'booking_status', 'created_at', 'updated_at'
        ]

    def validate_parking_spot(self, value):
        request = self.context['request']
        if Booking.objects.filter(parking_spot=value, user=request.user).exists():
            raise serializers.ValidationError(
                "You have already booked this parking spot.")
        return value

    def validate_parking_time(self, value):
        if value not in range(1, 9):
            raise serializers.ValidationError(
                "Parking time must be between 1 and 8 hours.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['user'] = owner
        return super().create(validated_data)
