import wx
import os
import pickle

from PIL import Image

library_path = f"saved/"


def pickle_save(data):
    """Pickle animu data after converting animu image file to PIL Image"""
    pkl_path = f"{library_path}{str(data.mal_id)}.pkl"

    if os.path.isfile(pkl_path):
        return "Animu already saved"
    else:
        with open(pkl_path, "wb") as file_handler:
            # Higher the protocol, the newer the python version needed (but the best optimized with the most features and support)
            # protocol 4 supports python 3.4+ (3.8 add protocol 5)

            pickle.dump(data, file_handler, protocol=4)

            return "Animu saved"


def convert_pil_img_to_wx_img(unpickled_pil_img):
    """Python Image Library Image object converted into a wx Image object"""
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
    pkl_path = f"{library_path}{file_id}"
    with open(pkl_path, "rb") as file_handler:
        data = pickle.load(file_handler)
        return data

    print("Error in loading data")


def load_library():
    """Returns a list of anime/manga names and a list with the corresponding saved anime/manga objects

    Returns:
        [list]: list of anime/manga titles
        [list]: list of anime/manga objects

    example return:
    [
        name1,
        name2,
        etc...
    ],

    [
        anime/manga_object1,
        anime/manga_object2,
        etc...
    ]

    """
    library_list = os.listdir(library_path)

    library = []
    name_list = []

    # If library not empty, load library
    if len(library_list) > 0:
        for item in library_list:

            animu_obj = pickle_load(item)
            library.append(animu_obj)

            # Shorten long titles and format for display
            if len(animu_obj.title) > 28:
                name_list.append(f"{animu_obj.title[:27]}.. [{animu_obj.type}]")
            else:
                name_list.append(f"{animu_obj.title} [{animu_obj.type}]")

        return name_list, library
    else:
        # Used to check if library is empty
        return None, None

