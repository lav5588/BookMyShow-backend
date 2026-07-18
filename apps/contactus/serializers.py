from rest_framework.serializers import ModelSerializer

from .models import ContactUsQuery


class ContactUsQuerySerializer(ModelSerializer):
    """
    Serializer for the ContactUsQuery model to handle POST requests.
    """

    class Meta:
        model = ContactUsQuery
        fields = ["id", "email", "query", "created_at"]
        read_only_fields = ["id", "created_at"]
