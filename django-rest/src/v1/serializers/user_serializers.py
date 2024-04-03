from src.v1.models import User

from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_employee",
        ]

    def validate(self, data):
        """
        Validate the data:
        - Check if all fields are provided
        - Lowercase all string fields
        - Check if email and phone are unique
        """
        # Check if all fields are provided
        missing_fields = set(self.fields) - set(data)
        if missing_fields:
            raise serializers.ValidationError(
                {field: "This field is required." for field in missing_fields}
            )

        # Lowercase all string fields
        data = {k: v.lower() if isinstance(v, str) else v for k, v in data.items()}

        # Check if email and phone are unique
        if User.objects.filter(email=data['email'], is_active=True).exists():
            raise serializers.ValidationError({"email": "This email is already taken."})

        if User.objects.filter(phone=data['phone'], is_active=True).exists():
            raise serializers.ValidationError({"phone": "This phone is already taken."})

        return data

    def create(self, validated_data):
        """
        Create a new user.
        """
        return User.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.
    """
    user_id = serializers.IntegerField(read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        Validate the data:
        - Check if username and password are provided
        - Authenticate the user
        - Create or retrieve the token for the user
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                # Set token expiration time (e.g., 7 days from now)
                expiration_time = timezone.now() + timedelta(days=7)

                # Create or retrieve the token for the authenticated user
                token, _ = Token.objects.get_or_create(user=user)
                token.created = timezone.now()
                token.expires = expiration_time
                token.save()

                # Return the token in Bearer token format
                return {
                    'user_id': user.id,
                    'token': 'Token ' + token.key,
                }
            else:
                raise serializers.ValidationError({"detail": "Wrong username or password."})
        else:
            raise serializers.ValidationError({"detail": "Must include 'username' and 'password'."})


class DetailUserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving the details of a user.
    """
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_employee"
        ]


class ListUserSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all users.
    """
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
