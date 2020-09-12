import wx
import os
import pickle

from PIL import Image

library_path = f"saved/"


def pickle_save(data, image):
    """Pickle animu data after converting animu image file to PIL Image"""
    pkl_path = f"{library_path}{str(data.mal_id)}.pkl"

    image = Image.open(image)

    if os.path.isfile(pkl_path):
        return "Animu already saved"
    else:
        with open(pkl_path, "wb") as file_handler:
            # Higher the protocol, the newer the python version needed (but the best optimized with the most features and support)
            # protocol 4 supports python 3.4+ (3.8 add protocol 5)

            pickle.dump(image, file_handler, protocol=4)
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
        etc...
    ],

    [
        animu_object1,
        animu_object2,
        etc...
    ],

    [
        PIL_image1,
        PIL_image2,
        etc...
    ]

    name -> see jikan_controller.py -> Anime/Manga self.title
    wx_image -> see convert_pil_img_to_wx_img function above
    animu_object -> see jikan_controller.py

    """
    library_list = os.listdir(library_path)

    library = []
    name_list = []

    # If library not empty, load library
    if len(library_list) > 0:
        for item in library_list:

            image, animu_obj = pickle_load(item)
            library.append((image, animu_obj))

            # Shorten long titles and format for display
            if len(animu_obj.title) > 28:
                name_list.append(f"{animu_obj.title[:27]}.. [{animu_obj.type}]")
            else:
                name_list.append(f"{animu_obj.title} [{animu_obj.type}]")

        # Separate image/object pair [(animu_img1, animu_obj1), (animu_img2, animu_obj2), etc.]
        library_objects = []
        library_images = []
        for animu_tuple in library:
            library_images.append(animu_tuple[0])
            library_objects.append(animu_tuple[1])

        return name_list, library_objects, library_images
    else:
        # Used to check if library is empty
        return None, None, None

