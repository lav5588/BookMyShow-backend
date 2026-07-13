from django import forms

from apps.movie.models import Language, Movie

from .models import Slot


class SlotAdminForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide all languages initially
        self.fields["language"].queryset = Language.objects.none()

        movie = None

        # Editing existing slot
        if self.instance.pk:
            movie = self.instance.movie

        # Form submitted
        elif self.data.get("movie"):
            try:
                movie = Movie.objects.get(pk=self.data["movie"])
            except (Movie.DoesNotExist, ValueError):
                pass

        if movie:
            self.fields["language"].queryset = movie.languages.all()
