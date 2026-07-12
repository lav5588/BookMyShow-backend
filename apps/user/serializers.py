from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from .models import User


class UserSerializer(ModelSerializer):
    """
    Serializer for the User Model
    handles password write only serialization
    """

    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "last_login",
            "is_staff",
            "is_superuser",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        """
        Creates a new User instance with the provided validated data
        sets the password using set_password method
        """
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(Serializer):
    """
    Serializer for changing a user's password
    Requires both old and new password
    """

    old_password = CharField(required=True)
    new_password = CharField(required=True)
    confirm_password = CharField(required=True)

    def validate(self, attrs):
        isNewAndConfirmPasswordSame = attrs["new_password"] == attrs["confirm_password"]
        if not isNewAndConfirmPasswordSame:
            raise ValidationError("new password and confirm password should be same")
        return attrs


class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "phone_number", "email", "profile_pic"]
