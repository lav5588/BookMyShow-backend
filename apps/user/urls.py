from django.urls import path

from .views import (
    ChangePasswordView,
    CustomTokenRefreshView,
    LoginUserView,
    LogoutView,
    RegisterUserView,
    UpdateUserProfileView,
    UserProfileView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh-token"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("update-profile/", UpdateUserProfileView.as_view(), name="update-profile"),
]
