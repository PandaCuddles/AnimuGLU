import os
import requests

from io import BytesIO
from PIL import Image
from os.path import isdir
from os import mkdir

from jikanpy import Jikan
from dateutil import parser
from pubsub import pub

import json


# Default local api url if using a local setup
# jikan_api_url = "http://localhost:8080/v3"

# Default online api if not using local setup (has restrictions)
jikan_api_url = "https://api.jikan.moe/v3"

jikan = Jikan(selected_base=jikan_api_url)


class Animu:
    """Object representing either a single manga or a single anime"""
    def __init__(self, info_dict : dict, type_is : str, loading: bool):
        """Create Animu object from Jikan search results"""
        self.mal_id = info_dict["mal_id"]
        self.animu = info_dict["title"]
        self.url = info_dict["url"]
        self.image_url = info_dict["image_url"]
        self.title = info_dict["title"]
        self.synopsis = info_dict["synopsis"]
        self.type = info_dict["type"]
        self.score = info_dict["score"]
        self.start_date = info_dict["start_date"]
        self.end_date = info_dict["end_date"]
        self.members = info_dict["members"]

        if type_is == "Anime":
            self.search_type = type_is
            self.episodes = info_dict["episodes"]
            self.rated = info_dict["rated"]
            self.airing = info_dict["airing"]
            if not loading:
                self.anime_formatting()
            self.anime_list()

        if type_is == "Manga":
            self.search_type = type_is
            self.publishing = info_dict["publishing"]
            self.chapters = info_dict["chapters"]
            self.volumes = info_dict["volumes"]
            if not loading:
                self.manga_formatting()
            self.manga_list()

        if loading:
            self.image = info_dict["image"]
            self.genre = info_dict["genre"]
            self.json = info_dict["json"]
            self.library = info_dict["library"]
            self.info_list.append(("Genre", self.genre))
        else:
            self.image = None
            self.genre = None
            self.json = None
            self.library = None
            self.general_formatting()
            self.get_image()

    def anime_list(self):
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

    def manga_list(self):
        self.info_list = [
            ("Id", self.mal_id),
            ("Title", self.title),
            ("Status", self.publishing),
            ("Type", self.type),
            ("Chapters", self.chapters),
            ("Volumes", self.volumes),
            ("Score", self.score),
            ("Start Date", self.start_date),
            ("End Date", self.end_date),
            ("Members", self.members),
        ]

    def get_image(self):
        try:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                self.image = response.content

        except requests.ConnectionError as e:
            e_msg = f"Could not download {self.title}: {e}"
            print(e_msg)
            

    def general_formatting(self):
        # Score
        if self.score == 0:
            self.score = "None"
        else:
            self.score = str(self.score)

        # Start Date
        if self.start_date:
            par = parser.parse(self.start_date)
            self.start_date = f"{par.strftime('%b')} {str(par.day)}, {str(par.year)}"
        else:
            self.start_date = "?"

        # End Date
        if self.end_date:
            par = parser.parse(self.end_date)
            self.end_date = f"{par.strftime('%b')} {par.day}, {par.year}"
        else:
            self.end_date = "?"

    def anime_formatting(self):
        # Airing
        if self.airing:
            self.airing = "True"
        else:
            self.airing = "No"

        # Episodes
        if self.episodes:
            self.episodes = str(self.episodes)
        else:
            self.episodes = "Unknown"

    def manga_formatting(self):
        # Publishing
        if self.publishing:
            self.publishing = "Publishing"
        else:
            self.publishing = "Finished"

        # Chapters
        if self.chapters:
            self.chapters = str(self.chapters)
        else:
            self.chapters = "Unknown"
        
        # Volumes
        if self.volumes:
            self.volumes = str(self.volumes)
        else:
            self.volumes = "Unknown"


def detailed_search(mal_id : int, type_is : str) -> dict:
    """Search for specific MAL id

    Args:
        animu_id (int): MAL id
        type_id (string): either 'Anime' or 'Manga', specifying Jikan search method

    Returns:
        dict: dictionary created from json formatted search results
    """

    if type_is == "Anime":
        details = jikan.anime(mal_id)
    elif type_is == "Manga":
        details = jikan.manga(mal_id)
    else:
        print("Detail search: Error saving")
        return None

    return details


def basic_search(animu_type : str, name : str, page_num : int=1):

    animu_obj_list = []
    # name list corresponds to index of object list
    animu_name_list = []

    # Loading message for user
    pub.sendMessage(
        "main_GUI-AnimuFrame", status_text="  Loading... (may take a moment)",
    )

    # Search limit: 2 (Increase if on fast internet)
    try:
        results = jikan.search(
                               animu_type.lower(),
                               name,
                               page=page_num,
                               parameters={"limit": 2})
    except Exception as e:
        print(e)
        pub.sendMessage("main_GUI-AnimuFrame", status_text="Search failed")
        return None, None

    # Create Anime/Manga objects based on search results
    for result in results["results"]:

        # Create object from anime/manga and download and store cover image inside the object
        if animu_type == "Anime":
            animu_obj = Animu(result, "Anime", False)
        if animu_type == "Manga":
            animu_obj = Animu(result, "Manga", False)

        animu_obj_list.append(animu_obj)
        animu_name_list.append(animu_obj.title)

    # Return list of animu objects and list of associated names
    pub.sendMessage("main_GUI-AnimuFrame", status_text="  Done")
    return animu_name_list, animu_obj_list
