import os
import requests
import shutil
import pickle

program_dir = os.getcwd()


def mk_dir(dir_name):

    dir_path = f"{program_dir}/{dir_name}"

    # Checks if directory exists
    exists = os.path.isdir(dir_path)

    # If directory missing, create a new one
    if not (exists):
        try:
            os.mkdir(dir_path)
        except OSError:
            print(f"Failed create folder: {dir_path}")
        else:
            print(f"Created folder: {dir_path}")
    else:
        print(f"Folder already exists: {dir_path}")


def store_animu(animu_obj):

    # Saves all the animu objects in a single file called animu_db.pkl
    animu_db = f"{program_dir}/animu_db.pkl"

    print(f"Storing animu info: {animu_obj.title}")

    with open(animu_db, "ab") as db_file_handler:
        """Higher the protocol, the newer the python version needed (but the best optimized with the most features and support)
        protocol 4 supports python 3.4+ (3.8 add protocol 5)
        """
        pickle.dump(animu_obj, db_file_handler, protocol=4)

    # Just a spacer for the debug messages
    print()


# An animu_obj is anything that deals with anime or manga
def dl_image(animu_obj):
    """Download anime/manga cover image

    Args:
        animu_obj (Anime/Manga): Object containing information on a particular anime/manga, see jikan_controller.py

    Returns:
        None: Return only if the anime/manga cover image has been downloaded already
    """

    # Directory for mal animu images (saved as "prg_dir/images/mal_id.jpg")
    img_path = f"{program_dir}/images/{str(animu_obj.mal_id)}.jpg"

    # Checks if the image already exists
    pre_check = os.path.isfile(img_path)
    if pre_check:
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
