from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'coordinates', 'availability', 'capacity',
                  'available_space', 'price', 'time_restrictions')
