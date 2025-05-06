from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'name', 'email', 'image', 'username', 'password',   #'is_staff', 
        ]
        read_only_fields = [
            'id', 'name', 'image', 'username',  # 'is_staff',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data.get('name', ''),
            email=validated_data['email'],
            username=validated_data['email'].split('@')[0],
            password=validated_data.get('password'),
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
