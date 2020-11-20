import dlsv
import os


from jikanpy import Jikan
from dateutil import parser
from pubsub import pub


# Default local api url if using a local setup
# jikan_api_url = "http://localhost:8080/v3"

# Default online api if not using local setup (has restrictions)
jikan_api_url = "https://api.jikan.moe/v3"

jikan = Jikan(selected_base=jikan_api_url)


# Base program directory
prg_directory = os.getcwd()

""" Animu object

A python object representing either a single manga or a single anime.

"""


class Manga:
    def __init__(self, manga_dict):
        """Create Manga object from Jikan search results, formatted from json->dict"""
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
        self.image = None
        self.searchType = "Manga"

        # Format the manga details before creating the information list
        self.format()

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
    
    def format(self):
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


class Anime:
    def __init__(self, anime_dict):
        """Create Anime (animation) object from Jikan search results, formatted from json->dict"""
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
        self.image = None
        self.searchType = "Anime"

        # Format the anime details before creating the information list
        self.format()

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

    def format(self):
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

        # Score
        if self.score == 0:
            self.score = "None"
        else:
            self.score = str(self.score)

        # Start Date
        if self.start_date:
            par = parser.parse(self.start_date)
            self.start_date = f"{par.strftime('%b')} {par.day}, {par.year}"
        else:
            self.start_date = "?"

        # End Date
        if self.end_date:
            par = parser.parse(self.end_date)
            self.end_date = f"{par.strftime('%b')} {par.day}, {par.year}"
        else:
            self.end_date = "?"


def detailed_search(animu_id, istype):
    """Search for specific MAL id

    Args:
        animu_id (int): MAL id
        istype (string): either 'Anime' or 'Manga', specifying Jikan search method

    Returns:
        dict: dictionary created from json formatted search results
    """

    if istype == "Anime":
        details = jikan.anime(animu_id)
    elif istype == "Manga":
        details = jikan.manga(animu_id)
    else:
        print(
            "Error occurred with detailed search while saving: check jikan_controller.py"
        )
        return None

    return details


def basic_search(animu_type, name, page_num=1):

    animu_obj_list = []
    # name list corresponds to index of object list
    animu_name_list = []

    # Loading message for user
    pub.sendMessage(
        "main_GUI-AnimuFrame", status_text="  Loading... (may take a while)",
    )

    # Search limit: 2 (Increase if on fast internet)
    try:
        results = jikan.search(
            animu_type.lower(), name, page=page_num, parameters={"limit": 2}
        )
    except Exception as e:
        print(e)
        pub.sendMessage("main_GUI-AnimuFrame", status_text="Search failed")
        return None, None

    # Create Anime/Manga objects based on search results
    for result in results["results"]:

        # Create object from anime/manga and download and store cover image inside the object
        if animu_type == "Anime":
            animu_obj = Anime(result)
            animu_obj.image = dlsv.dl_img(animu_obj)
        if animu_type == "Manga":
            animu_obj = Manga(result)
            animu_obj.image = dlsv.dl_img(animu_obj)

        animu_obj_list.append(animu_obj)
        animu_name_list.append(animu_obj.title)

    # Return list of animu objects and list of associated names
    pub.sendMessage("main_GUI-AnimuFrame", status_text="  Done")
    return animu_name_list, animu_obj_list
