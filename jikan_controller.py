import os
import dlsv
from jikanpy import Jikan
from pubsub import pub


# Change url depending on if a local setup is used or not
jikan_api_url = "http://localhost:8080/v3"

jikan = Jikan(selected_base=jikan_api_url)


# Base program directory
prg_directory = os.getcwd()
default_image_dir = f"{prg_directory}/images/"

""" Animu Object

A python object representing either a single manga or a single anime.

"""


class Manga:
    def __init__(self, manga_dict):
        self.manga = manga_dict["title"]

        self.mal_id = manga_dict["mal_id"]
        self.url = manga_dict["url"]
        self.image_url = manga_dict["image_url"]
        self.title = manga_dict["title"]
        self.publishing = manga_dict["publishing"]
        self.synopsis = manga_dict["synopsis"]
        self.type = manga_dict["type"]
        self.chapters = manga_dict["chapters"]
        self.volumes = manga_dict["volumes"]
        self.score = manga_dict["score"]
        self.start_date = manga_dict["start_date"]
        self.end_date = manga_dict["end_date"]
        self.members = manga_dict["members"]
        self.localImage = f"{default_image_dir}{self.mal_id}.jpg"

        self.info_list = [
            ("Id", self.mal_id),
            ("Title", self.title),
            ("Publishing", self.publishing),
            ("Type", self.type),
            ("Chapters", self.chapters),
            ("Volumes", self.volumes),
            ("Score", self.score),
            ("Start Date", self.start_date),
            ("End Date", self.end_date),
            ("Members", self.members),
        ]


class Anime:
    def __init__(self, anime_dict):
        self.anime = anime_dict["title"]

        self.mal_id = anime_dict["mal_id"]
        self.url = anime_dict["url"]
        self.image_url = anime_dict["image_url"]
        self.title = anime_dict["title"]
        self.airing = anime_dict["airing"]
        self.synopsis = anime_dict["synopsis"]
        self.type = anime_dict["type"]
        self.episodes = anime_dict["episodes"]
        self.score = anime_dict["score"]
        self.start_date = anime_dict["start_date"]
        self.end_date = anime_dict["end_date"]
        self.members = anime_dict["members"]
        self.rated = anime_dict["rated"]
        self.localImage = f"{default_image_dir}{self.mal_id}.jpg"

        self.info_list = [
            ("Id", self.mal_id),
            ("Title", self.title),
            ("Airing", self.airing),
            ("Type", self.type),
            ("Episodes", self.episodes),
            ("Score", self.score),
            ("Start Date", self.start_date),
            ("End Date", self.end_date),
            ("Members", self.members),
            ("Rated", self.rated),
        ]


def detailed_search(animu_id):
    details = jikan.anime(animu_id)

    """
    genres = []
    for genre in details["genres"]:
        genres.append(genre["name"])
        # print(genre["name"])

    print(", ".join(genres))
    """

    return details


def basic_search(animu_type, name, page_num=1):
    animu_obj_list = []
    animu_name_list = []

    """Loading message for user"""
    pub.sendMessage(
        "main_GUI-AnimuFrame",
        status_text="  Loading... (this may take a while, depending on your internet connection)",
    )

    """Limited search results to 2 items (I have slow internet at the moment)"""
    results = jikan.search(
        animu_type.lower(), name, page=page_num, parameters={"limit": 2}
    )

    for result in results["results"]:

        if animu_type == "Anime":
            animu_obj = Anime(result)
        if animu_type == "Manga":
            animu_obj = Manga(result)

        animu_obj_list.append(animu_obj)
        animu_name_list.append(animu_obj.title)

    # Return animu names and the animu objects associated with each name
    pub.sendMessage("main_GUI-AnimuFrame", status_text="  Done")
    return animu_name_list, animu_obj_list


def check_download(animu_obj):
    check = os.path.isfile(f"{default_image_dir}/{animu_obj.mal_id}.jpg")
    if check:
        return True
    else:
        return False


def all_img_dl(animu_obj_list):
    dlsv.image_all_download(animu_obj_list)


def single_img_dl(animu_obj):
    dlsv.dl_image(animu_obj)
