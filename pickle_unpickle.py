import wx
import os
import pickle

from PIL import Image

base_path = f"{os.getcwd()}/saved/"


def prepare_image(image):
    pass


def pickle_save(data, image):
    pkl_path = f"{base_path}{str(data.mal_id)}.pkl"

    # Create PIL image object (wx objects can't be pickled)
    image = Image.open(image)

    if os.path.isfile(pkl_path):
        return "Animu already saved"
    else:
        with open(pkl_path, "wb") as file_handler:
            pickle.dump(image, file_handler, protocol=4)
            pickle.dump(data, file_handler, protocol=4)

            return "Animu saved"


def convert_pil_img_to_wx_img(unpickled_pil_img):
    # Python Image Library Image object converted into a wx Image object
    pil_width = unpickled_pil_img.size[0]
    pil_height = unpickled_pil_img.size[1]
    wx_image = wx.Image(pil_width, pil_height)

    pil_image = unpickled_pil_img.convert("RGB")
    pil_image_data = pil_image.tobytes()

    wx_image.SetData(pil_image_data)

    return wx_image


def pickle_load(file_id):
    """load the pickled data of a specific anime/manga

    Args:
        id (str): filename of the anime/manga used to initially pickle the anime/manga
    """
    pkl_path = f"{base_path}{file_id}"
    with open(pkl_path, "rb") as file_handler:
        image = pickle.load(file_handler)

        image = convert_pil_img_to_wx_img(image)

        data = pickle.load(file_handler)
        return image, data

    print("Error in loading data")


def load_library():
    """Returns list of names and list of tuples for each saved animu

    Returns:
        [list]: list of anime/manga titles
        [list]: list of animu tuples with an image object and an animu object

    example return:
    [
        name1,
        name2,
        etc..
    ]

    [
        (wx_image1, animu_object1),
        (wx_image2, animu_object2),
        etc.
    ]

    name -> see main_jikan.py -> Anime/Manga self.title
    wx_image -> see PILConverterWxImg function above
    animu_object -> see main_jikan.py

    """
    library_list = os.listdir(base_path)
    library = []
    name_list = []
    if len(library_list) > 0:
        for item in library_list:

            image, animu_obj = pickle_load(item)
            library.append((image, animu_obj))
            name_list.append(f"{animu_obj.title} [{animu_obj.type}]")

        return name_list, library
    else:
        print("Nothing in Library")
        return None, None

