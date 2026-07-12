from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from . import constants
from .serializers import (
    ChangePasswordSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    """
    Handle HTTP POST request for user registration
    Request: email, name, phone_number, password
    Response: 201 user data | 400 validation errors
    """

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        response = Response(
            {**serializer.data, "access": str(refresh_token.access_token)},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            httponly=True,
            secure=False,
            max_age=constants.SESSION_COOKIE_MAX_AGE_SECONDS,
            samesite="Lax",
        )
        return response


class LoginUserView(TokenObtainPairView):
    """
    Custom login view that authenticates users via JWT and sets refresh token as HttpOnly cookie.

    Handles POST requests with user credentials to generate access/refresh token pair.
    Returns both tokens in response body (SimpleJWT default) AND sets refresh token
    in secure HttpOnly cookie for web clients.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.pop("refresh")

            response.set_cookie(
                key="refresh",
                value=refresh_token,
                httponly=True,
                secure=False,
                max_age=constants.SESSION_COOKIE_MAX_AGE_SECONDS,
                samesite="lax",
            )
            return response
        return Response(
            {"error": "Failed to Login"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(TokenBlacklistView):
    """
    handle post request for logout
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"error": "No refresh token"}, status=400)
        request.data.update({"refresh": refresh_token})
        response = super().post(request, *args, **kwargs)
        response = Response(
            {"message": "You have logged out successfully"}, status=response.status_code
        )
        response.delete_cookie("refresh")
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    handle post request for refresh the tokens
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response(
                {"message": "Refresh token missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.data.update({"refresh": refresh_token})

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.pop("refresh")

            response.set_cookie(
                key="refresh",
                value=refresh_token,
                httponly=True,
                secure=False,
                max_age=constants.SESSION_COOKIE_MAX_AGE_SECONDS,
                samesite=None,
            )
            return response

        return Response(
            {"message": "token refresh failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ["patch"]

    """
    handle patch request for changing password
    """

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        user = request.user

        if not user.check_password(raw_password=old_password):
            return Response(
                {
                    "error": "password not match",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"success": "password changed successfully"}, status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieve authenticated user's profile.
    """

    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserProfileView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    http_method_names = ["patch"]

    def get_object(self):
        return self.request.user
