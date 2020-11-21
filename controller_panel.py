import jikan_controller
import pickle_unpickle

import json
import shelve  # For saving and loading sort config
import wx

from io import BytesIO
from os.path import isfile
from os import remove
from pubsub import pub

library_path = "library/"

# TODO: Redo Controller Panel docstring
class ControllerPanel(wx.Panel):
    """Controller Panel containing key program logic, and acts as a 'main hub' for different parts of the program"""

    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self.i_cant = "Uh, I can't, I'm buying clothes"
        self.alright = "Aight, well hurry up and come over here"
        self.cant_find_them = "I can't find them"
        self.what = "What do you mean you can't find them?"
        self.only = "I can't find them, there's only soup"


        self.animu_list_default = None  # keep original list for sorting purposes
        self.current_animu_list = None

        self.name_list_default = None  # keep original list for sorting purposes
        self.name_list = None

        # Library stuff
        self.library_type = 0
        self.in_library = False

        # Sorting stuff
        self.disable_sort = False  # Disable sorting when in an empty library
        self.sort = 1  # Used for current sorting type
        self.library_type_l = [
            "finished",
            "unfinished",
            "wishlist",
        ]  # Used for saving and loading library

        self.sort_status = (
            f"Library ({self.library_type_l[self.library_type]}): Unsorted"
        )

        self.selected_object = None
        self.selected_index = None

        self.lib_gen = self.lib_generator()

        pub.subscribe(self.show_search_results, "show_search_results")
        pub.subscribe(self.show_library,        "show_library")
        pub.subscribe(self.delete_selected,     "delete_selected")
        pub.subscribe(self.save_selected,       "save_selected")
        pub.subscribe(self.view_selected,       "view_selected")
        pub.subscribe(self.import_list,         "import_list")
        pub.subscribe(self.sort_library,        "sort_library")
        pub.subscribe(self.set_sort,            "set_sort")
        pub.subscribe(self.save_sort,           "save_sort")
        pub.subscribe(self.save_lib_type,       "save_lib_type")
        pub.subscribe(self.set_lib_type,        "set_lib_type")
        pub.subscribe(self.lib_next,            "next_library")

    def lib_generator(self):
        library = 0
        while True:
            if library == 3:
                library = 0
            yield library
            library += 1

    def lib_next(self):
        """Go to next library type option and display for either saving or loading library"""

        if self.in_library:
            self.library_type = next(self.lib_gen)
            pub.sendMessage("show_library")
        else:
            self.library_type = next(self.lib_gen)
            status = f"Save to: {self.library_type_l[self.library_type]} library"
            pub.sendMessage(
                "main_GUI-AnimuFrame",
                status_text=status,
            )

    def set_lib_type(self):
        """Load config value for last used library type"""
        with shelve.open("config.pkl") as db:
            self.library_type = db["library_type"]

    def save_lib_type(self):
        """Save config value for last used library type"""
        with shelve.open("config.pkl") as db:
            db["library_type"] = self.library_type

    def set_sort(self):
        """Load config value for last used sorting type"""
        with shelve.open("config.pkl") as db:
            self.sort = db["sort_type"]

    def save_sort(self):
        """Save config value for last used sorting type"""
        with shelve.open("config.pkl") as db:
            db["sort_type"] = self.sort

    def show_search_results(self, names, animu_objects):
        """Send results to listbox and download cover images

        Args:
            animu_objects : [obj1, obj2, obj3]

            names : ["name1", "name2", "name3"]

        """
        self.in_library = False
        self.current_animu_list = animu_objects

        # Reset sorting library variables
        self.animu_list_default = None
        self.name_list_default = None
        self.name_list = None

        pub.sendMessage("populate_listbox", name_list=names)

        # Send message for current library to save anime/manga to
        pub.sendMessage(
            "main_GUI-AnimuFrame",
            status_text=f"Save to: {self.library_type_l[self.library_type]} library",
        )

    def import_list(self, import_list):
        formatted_import_list = []
        for item in import_list:
            if " -a" in item:
                formatted_import_list.append((item[0:-3], "Anime"))
            elif " -m" in item:
                formatted_import_list.append((item[0:-3], "Manga"))
            else:
                with open("error.log", "a") as file:
                    file.write(
                        f"Line {import_list.index(item)}: {item} :FAILED (Formatting Error)\n"
                    )

        for item in formatted_import_list:
            name = item[0]
            kind = item[1]
            _, objs = jikan_controller.basic_search(kind, name)
            if objs:
                self.selected_object = objs[0]
                self.save_selected()
        pub.sendMessage(
            "main_GUI-AnimuFrame",
            status_text="Finished Importing",
        )

    def show_library(self):
        """If library not empty, load and display library

        If library is empty, clear listbox (in case search was done beforehand)
        and display message that library is empty

        """

        name_list, library_objects = pickle_unpickle.load_library(
            self.library_type_l[self.library_type]
        )

        if name_list == None or library_objects == None:
            # Clears the listbox by sending empty list
            pub.sendMessage("populate_listbox", name_list=name_list)
            pub.sendMessage(
                "main_GUI-AnimuFrame",
                status_text=f"Nothing in library ({self.library_type_l[self.library_type]}) yet",
            )
            self.disable_sort = True

            return None
        else:
            self.disable_sort = False
            # If you are in the library and click the library button again, just load previous results
            if self.in_library:
                self.current_animu_list = library_objects
                self.name_list = name_list

                # Save second copy of library objects for sorting purposes
                self.animu_list_default = library_objects
                self.name_list_default = name_list
                pub.sendMessage("populate_listbox", name_list=self.name_list)

                if self.sort != 0:
                    self.sort -= 1
                elif self.sort == 0:
                    self.sort = 3

                self.sort_library()
            else:
                # In library, so set value to reflect that
                self.in_library = True

                self.current_animu_list = library_objects
                self.name_list = name_list

                # Save second copy of library objects for sorting purposes
                self.animu_list_default = library_objects
                self.name_list_default = name_list

                # Sort functions increment sort counter by 1 each time,
                # so loading library with saved sort value needs to decrement
                # by 1 before sorting library
                if self.sort != 0:
                    self.sort -= 1
                elif self.sort == 0:
                    self.sort = 3

                self.sort_library()

    def configure_save(self, save_obj, details):
        """Append formatted genre list and full synopsis to animu object

        Args:
            save_obj (animu obj): An Anime or Manga object instance
            details (dict): jikan api search result
        """
        if not details:
            return

        genres = []
        for genre in details["genres"]:
            genres.append(genre["name"])

        genre_string = ", ".join(genres)
        save_obj.info_list.append(("Genre", genre_string))
        save_obj.synopsis = details["synopsis"]
        save_obj.json = json.dumps(details)

    def save_selected(self):

        """Check if program is in search mode, and if so, save selected anime/manga"""
        if not self.in_library and self.selected_object:
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saving...")

            # Retrieve more detailed info on selected item
            expanded_details = jikan_controller.detailed_search(
                self.selected_object.mal_id, self.selected_object.search_type
            )
            # Add extra details to animu object before pickling
            self.configure_save(self.selected_object, expanded_details)

            pickle_unpickle.pickle_save(
                self.selected_object, self.library_type_l[self.library_type]
            )

            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saved!")
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="No search item selected"
            )

    def delete_selected(self):
        """Delete selection, reload library, clear information section of app"""
        if self.in_library and not (self.selected_index == None):

            animu = self.current_animu_list[self.selected_index]

            remove(
                f"{library_path}{self.library_type_l[self.library_type]}/{str(animu.mal_id)}.pkl"
            )
            pub.sendMessage("show_library")
            pub.sendMessage("display_synopsis", synopsis=None)
            pub.sendMessage("display_details", item_list=None)
            pub.sendMessage("set_webpage", animu_url=None)
            pub.sendMessage("display_cover", wx_image=None)

        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame",
                status_text="No library item selected",
            )

    def view_selected(self, selected_index):
        """Take selected manga/anime and display its information"""
        self.selected_index = selected_index
        self.selected_object = self.current_animu_list[selected_index]
        image = wx.Image(BytesIO(self.selected_object.image))

        pub.sendMessage("display_synopsis", synopsis=self.selected_object.synopsis)
        pub.sendMessage("display_details", item_list=self.selected_object.info_list)
        pub.sendMessage("set_webpage", animu_url=self.selected_object.url)
        pub.sendMessage("display_cover", wx_image=image)

    # TODO: Cleanup/streamline sorting and formatting
    def sort_library(self):
        """Sort current library
        Zip current library up (contains tuples of (name, object))
        Sort by name (using the name inside each tuple) and/or
        sort by type (using the type attribute inside each object)
        Unzip sorted library
        Display sorted library
        """

        if self.in_library and not (self.disable_sort):
            if self.sort == 0:
                self.current_animu_list = self.animu_list_default
                self.name_list = self.name_list_default
                pub.sendMessage("populate_listbox", name_list=self.name_list)
                pub.sendMessage(
                    "main_GUI-AnimuFrame",
                    status_text=f"Library ({self.library_type_l[self.library_type]}): Unsorted",
                )
                self.sort += 1
                self.sort_status = (
                    f"Library ({self.library_type_l[self.library_type]}): Unsorted"
                )
            elif self.sort == 1:
                self.current_animu_list = self.animu_list_default
                self.name_list = self.name_list_default

                unsorted = zip(self.name_list_default, self.animu_list_default)
                name_sorted = sorted(unsorted, key=lambda k: k[0])
                self.name_list, self.current_animu_list = zip(*name_sorted)
                pub.sendMessage("populate_listbox", name_list=self.name_list)
                pub.sendMessage(
                    "main_GUI-AnimuFrame",
                    status_text=f"Library ({self.library_type_l[self.library_type]}): Sorted by Name",
                )
                self.sort += 1
                self.sort_status = f"Library ({self.library_type_l[self.library_type]}): Sorted by Name"

            elif self.sort == 2:
                # Reset lists from name sorting and format for type sorting
                self.current_animu_list = self.animu_list_default
                self.name_list = self.name_list_default

                # Format names, then sort by type
                self.format_type_sort()

                unsorted = zip(self.name_list, self.current_animu_list)
                type_sorted = sorted(unsorted, key=lambda k: k[1].type)
                self.name_list, self.current_animu_list = zip(*type_sorted)
                pub.sendMessage("populate_listbox", name_list=self.name_list)
                pub.sendMessage(
                    "main_GUI-AnimuFrame",
                    status_text=f"Library ({self.library_type_l[self.library_type]}): Sorted by Type",
                )
                self.sort += 1
                self.sort_status = f"Library ({self.library_type_l[self.library_type]}): Sorted by Type"

            elif self.sort == 3:
                unsorted = zip(self.name_list_default, self.animu_list_default)
                name_sorted = sorted(unsorted, key=lambda k: k[0])

                # Unzip, format names, rezip and sort by type
                self.name_list, self.current_animu_list = zip(*name_sorted)
                self.format_type_sort()

                name_formatted = zip(self.name_list, self.current_animu_list)
                type_sorted = sorted(name_formatted, key=lambda k: k[1].type)
                self.name_list, self.current_animu_list = zip(*type_sorted)
                pub.sendMessage("populate_listbox", name_list=self.name_list)
                pub.sendMessage(
                    "main_GUI-AnimuFrame",
                    status_text=f"Library ({self.library_type_l[self.library_type]}): Sorted by Name and Type",
                )
                self.sort_status = f"Library ({self.library_type_l[self.library_type]}): Sorted by Name and Type"
                self.sort = 0

            else:
                print("Error with sort function in controller_panel")
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame",
                status_text="Cannot sort unless in library",
            )

    def format_type_sort(self):
        new_names = []

        for name in self.name_list:
            index = self.name_list.index(name)  # Get index of current anime/manga
            animu_obj = self.current_animu_list[index]  # Get anime/manga object

            # Format names for displaying type sorted library
            if len(animu_obj.title) > 28:
                new_names.append(f"[{animu_obj.type}] {animu_obj.title[:28]}..")
            else:
                new_names.append(f"[{animu_obj.type}] {animu_obj.title} ")
        self.name_list = new_names

    def format_name_sort(self):
        for name in self.name_list:
            index = self.name_list.index(name)  # Get index of current anime/manga
            animu_obj = self.current_animu_list[index]  # Get anime/manga object

            # Format names for displaying name sorted library
            if len(animu_obj.title) > 28:
                self.name_list[index] = f"{animu_obj.title[:28]}.. [{animu_obj.type}]"
            else:
                self.name_list[index] = f"{animu_obj.title} [{animu_obj.type}]"
