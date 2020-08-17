import requests
import shutil
import pickle

from os.path import isdir, isfile
from os import mkdir


def mk_dir(dir_name):

    # If directory missing, create a new one
    if not isdir(dir_name):
        try:
            mkdir(dir_name)
        except OSError:
            print(f"Failed create folder: {dir_name}")
        else:
            print(f"Created folder: {dir_name}")


# An animu_obj is anything that deals with anime or manga
def dl_image(animu_obj):
    """Download anime/manga cover image

    Args:
        animu_obj (Anime/Manga): Object containing information on a particular anime/manga, see jikan_controller.py

    Returns:
        None: Return only if the anime/manga cover image has been downloaded already
    """

    # Directory for mal animu images (saved as "prg_dir/images/mal_id.jpg")
    img_path = f"images/{str(animu_obj.mal_id)}.jpg"

    # Checks if the image already exists
    if isfile(img_path):
        print(f"Animu image already saved: {animu_obj.title}")
        return

    # Send GET request for the image data
    # with requests.Session() as session uses a context manager for the request
    with requests.Session() as session:
        try:
            img_request = session.get(animu_obj.image_url, stream=True, timeout=10)
        except requests.exceptions.Timeout:
            print("Timeout occurred")

        # Image successfully retrieved
        if img_request.status_code == 200:

            # This enables decoding the content, so it can be saved to a file
            img_request.raw.decode_content = True

            print(f"Saving animu image: {animu_obj.title}")

            with open(img_path, "wb") as img_file_handler:
                # Copies the image binary data directly into the newly created image file
                shutil.copyfileobj(img_request.raw, img_file_handler)
                animu_obj.localImage = img_path
        else:
            print(f"Failed to retrieve image data: {animu_obj.title}")
