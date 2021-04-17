from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Employee, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims to returned token
        token["username"] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "nationality",
            "slack_user",
        )
