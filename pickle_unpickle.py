import os
import pickle
import wx

from PIL import Image

library_path = f"library/"


def pil_to_wx(img):
    """Convert PIL Image into a wx Image"""
    width = img.size[0]
    height = img.size[1]
    wx_image = wx.Image(width, height)

    wx_image.SetData(img.convert("RGB").tobytes())

    return wx_image

def pickle_save(data, lib_type):
    """Pickle anime/manga object"""
    pkl_path = f"{library_path}{lib_type}/{str(data.mal_id)}.pkl"

    if os.path.isfile(pkl_path):
        return "Already saved"
    else:
        with open(pkl_path, "wb") as file_handler:
            # Higher the protocol, the newer the python version needed (but the best optimized with the most features and support)
            # protocol 4 supports python 3.4+ (3.8 add protocol 5)

            pickle.dump(data, file_handler, protocol=4)

            return "Saved!"

def pickle_load(file_id, lib_type):
    """load the pickled data of a specific anime/manga

    Args:
        id (str): filename of the anime/manga used to initially pickle the anime/manga
    """
    pkl_path = f"{library_path}{lib_type}/{file_id}"
    with open(pkl_path, "rb") as file_handler:
        data = pickle.load(file_handler)
        return data

    print("Error in loading data")


def load_library(lib_type):
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
    if os.path.isdir(f"{library_path}{lib_type}/"):
        library_list = os.listdir(f"{library_path}{lib_type}/")
    else:
        return None, None

    library = []
    name_list = []

    # If library not empty, load library
    if len(library_list) > 0:
        for item in library_list:

            animu_obj = pickle_load(item, lib_type)
            library.append(animu_obj)

            # Shorten long titles and format for display
            if len(animu_obj.title) > 28:
                name_list.append(f"{animu_obj.title[:28]}.. [{animu_obj.type}]")
            else:
                name_list.append(f"{animu_obj.title} [{animu_obj.type}]")

        return name_list, library
    else:
        # Used to check if library is empty
        return None, None
