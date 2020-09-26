from os import mkdir
from os import remove
from os.path import isdir
from PIL import Image
from urllib import error, request


def dl_img(animu_obj):
    """Download anime/manga cover image and return Image object

    Args:
        animu_obj (Anime/Manga object): Object containing information on a particular anime/manga, see jikan_controller.py

    Returns:
        PIL Image: Cover image converted into a PIL image object
    """

    temp = "temp.jpg"
    try:
        url = request.urlretrieve(animu_obj.image_url, temp)
        img = Image.open(temp)
        # Data corruption occurs if temp image file not deleted before next image download
        remove(temp)
        return img
    except error.HTTPError as e:
        e_msg = f"Could not download {animu_obj.title}: {e}"
        print(e_msg)
        return


def mk_dir(dir_name):
    """Create directory for library and cover image downloads if missing"""
    if not isdir(dir_name):
        try:
            mkdir(dir_name)
        except OSError:
            print(f"Failed create folder: {dir_name}")
        else:
            print(f"Created folder: {dir_name}")
