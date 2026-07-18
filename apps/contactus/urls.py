from django.urls import path

from .views import ContactUsQueryCreateView

urlpatterns = [
    path("", ContactUsQueryCreateView.as_view(), name="contact-us-create"),
]
