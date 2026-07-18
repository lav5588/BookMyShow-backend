from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.contactus.models import ContactUsQuery


class ContactUsQueryCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("contact-us-create")

    def test_create_contact_us_query_success(self):
        """
        Test that a valid POST request successfully creates a contact query.
        """
        data = {
            "email": "test@example.com",
            "query": "This is a test query description.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactUsQuery.objects.count(), 1)
        query = ContactUsQuery.objects.first()
        self.assertEqual(query.email, "test@example.com")
        self.assertEqual(query.query, "This is a test query description.")

    def test_create_contact_us_query_invalid_email(self):
        """
        Test that an invalid email address returns validation error.
        """
        data = {
            "email": "invalid-email",
            "query": "This is a query with an invalid email address.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(ContactUsQuery.objects.count(), 0)

    def test_create_contact_us_query_missing_fields(self):
        """
        Test that missing required fields returns validation error.
        """
        data = {
            "email": "test@example.com"
            # 'query' field is missing
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("query", response.data)
        self.assertEqual(ContactUsQuery.objects.count(), 0)
