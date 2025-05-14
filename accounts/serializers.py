from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = [
        #     'id', 'name', 'email', 'image', 'username', 'password',   #'is_staff', 
        # ]
        # read_only_fields = [
        #     'id', 'name', 'image', 'username',  # 'is_staff',
        # ]
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     # 'email': {'required': True},
        #     'username': {'required': True},
            
        # }

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #         name=validated_data.get('name', ''),
    #         # username = validated_data.get('username', ''),
    #         # email=validated_data['email'],
    #         # username=validated_data['email'].split('@')[0],
    #         password=validated_data.get('password'),
    #     )
    #     return user


    def create(self, validated_data):
        """
        Create and return a new user instance with hashed password.
        """
        # Hash the password before saving
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user



    def update(self, instance, validated_data):
        """
        Update and return an existing user instance.
        """
        # instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.username = validated_data.get('username', instance.username)

        # Handle password update
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


