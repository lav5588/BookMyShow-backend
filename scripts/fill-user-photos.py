import requests

from apps.user.models import User


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


API_URL = "https://randomuser.me/api"
img_urls = []
users_count = User.objects.filter(profile_pic="").count()
for page in range(1, users_count + 1):
    response = requests.get(API_URL, params={"results": users_count})
    response.raise_for_status()
    data = response.json()
    img_urls.extend(user["picture"]["large"] for user in data["results"])

users = User.objects.filter(profile_pic="")
for user, imgage_url in zip(users, img_urls):
    user_path = f"public/users/{user.name}.webp"
    if download_image(imgage_url, user_path):
        user.profile_pic = user_path
        user.save()
        print(f"Updated {user.name}")


# # Important when images are already available but not link
# from apps.users.models import User
# from django.db.models.functions import Concat
# from django.db.models import F, Value
# User.objects.filter(profile_pic='').update(profile_pic=Concat(Value('public/users/'),F('name'),Value('.webp')))
