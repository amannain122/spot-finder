from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, User, Post, Bookings


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


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'coordinates', 'availability', 'capacity',
                  'available_space', 'price', 'time_restrictions')


class QRCodeSerializer(serializers.Serializer):
    data = serializers.CharField(max_length=200)



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['parking_id', 'parking_spot_no',]