import requests

from apps.movie.models import Movie


def download_image(img_url, save_as):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        with open(save_as, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Successfully downloaded: {save_as}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")
        return False


API_URL = "https://random.danielpetrica.com/api/random"

movies = Movie.objects.filter(movie_poster="").order_by("id")
for movie in movies:
    movie_path = f"public/movies/{movie.slug}.webp"
    if download_image(API_URL, movie_path):
        movie.movie_poster = movie_path
        movie.save()
        print(f"Updated {movie.id} {movie.name}")

# # Important when images are already available but not link
# from apps.movie.models import Movie
# from django.db.models.functions import Concat
# from django.db.models import F, Value
# Movie.objects.filter(movie_poster='').update(movie_poster=Concat(Value('public/movies/'),F('slug'),Value('.webp')))
