from io import BytesIO
from PIL import Image
from os.path import isdir
from os import (mkdir, remove)

import requests


def dl_img(animu_obj):
    """Download anime/manga cover image and return Image object

    Args:
        animu_obj (Anime/Manga object): Object containing information on a particular anime/manga, see jikan_controller.py

    Returns:
        PIL Image: Cover image converted into a PIL image object
    """

    try:
        response = requests.get(animu_obj.image_url)
        img = Image.open(BytesIO(response.content)) # Treats content like a file but purely in memory
        return img

    except requests.ConnectionError as e:
        e_msg = f"Could not download {animu_obj.title}: {e}"
        print(e_msg)
        return


def mk_dir(dir_name):
    """Creates a directory if it doesn't exist"""
    if not isdir(dir_name):
        try:
            mkdir(dir_name)
        except OSError:
            print(f"Failed create folder: {dir_name}")
        else:
            print(f"Created folder: {dir_name}")
