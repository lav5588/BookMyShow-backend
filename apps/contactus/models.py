from django.db import models


class ContactUsQuery(models.Model):
    """
    Represents a user contact submission containing an email and query details.
    """

    email = models.EmailField("email address")
    query = models.TextField("query description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Us Query"
        verbose_name_plural = "Contact Us Queries"

    def __str__(self):
        return f"{self.email} - {self.query[:30]}"
