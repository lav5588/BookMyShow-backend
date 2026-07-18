from rest_framework.generics import CreateAPIView

from .models import ContactUsQuery
from .serializers import ContactUsQuerySerializer


class ContactUsQueryCreateView(CreateAPIView):
    """
    API view to handle creation of a contact us query submission.
    """

    queryset = ContactUsQuery.objects.all()
    serializer_class = ContactUsQuerySerializer
