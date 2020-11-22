import jikan_controller
import load
import sql_cmd
from sql_cmd import set_config as update_config_database
from jikan_controller import detailed_search

import json
import shelve  # For saving and loading sort config
import wx

from io import BytesIO
from os.path import isfile
from os import remove
from pubsub import pub


class ControllerPanel(wx.Panel):
    """Controller Panel containing key program logic, and acts as a 'main hub' for different parts of the program"""

    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        # Buying clothes at the soup store
        self.i_cant         = "Uh, I can't, I'm buying clothes"
        self.alright        = "Aight, well hurry up and come over here"
        self.cant_find_them = "I can't find them"
        self.what           = "What do you mean you can't find them?"
        self.only           = "I can't find them, there's only soup"

        # Library stuff
        self.library_type = "finished"
        self.in_library   = False
        self.lib_gen = self.lib_generator()
        next(self.lib_gen) # Initialize generator

        # Config stuff
        self.conn = sql_cmd.setup("(startup) Database connection established")
        self.configs = sql_cmd.get_configs(self.conn)
        self.active = self.configs[self.library_type]

        # Display stuff
        self.animu_list = []
        self.name_list = []
        self.selected_object = None
        self.selected_index = None

        # Sorting stuff
        self.disable_sort = False  # Disable sorting when in an empty library
        self.sort         = self.active[1]      # Used for current sorting type
        self.sort_status = f"Library ({self.library_type}): Unsorted"

        # Controller stuff
        pub.subscribe(self.show_search_results, "show_search_results")
        pub.subscribe(self.show_library,        "show_library")
        pub.subscribe(self.delete_selected,     "delete_selected")
        pub.subscribe(self.save_selected,       "save_selected")
        pub.subscribe(self.view_selected,       "view_selected")
        pub.subscribe(self.import_list,         "import_list")
        pub.subscribe(self.sort_library,        "sort_library")
        pub.subscribe(self.lib_next,            "next_library")
        pub.subscribe(self.cleanup,             "cleanup")

    def lib_generator(self):
        index = 0
        library = ["finished", "unfinished", "wishlist"]
        while True:
            if index == 3:
                index = 0
            yield library[index]
            index += 1

    def cleanup(self):
        """Close database connection before exiting program"""
        self.conn.close()
        print("(shutdown) Database connection closed")

    def lib_next(self):
        """Go to next library type option and display for either saving or loading library"""
        if self.in_library:
            self.library_type = next(self.lib_gen)
            self.sort = self.configs[self.library_type][1]
            self.library_status(next(self.sort))
            pub.sendMessage("show_library")
        else:
            self.library_type = next(self.lib_gen)
            self.sort = self.configs[self.library_type][1]
            status = f"Save to: {self.library_type} library"
            pub.sendMessage("main_GUI-AnimuFrame", status_text=status)

    def show_search_results(self, names, animu_objects):
        """Send results to listbox and download cover images

        Args:
            animu_objects : [obj1, obj2, obj3]

            names : ["name1", "name2", "name3"]

        """
        self.in_library = False
        self.animu_list = animu_objects
        self.name_list = names

        pub.sendMessage("populate_listbox", name_list=self.name_list)
        pub.sendMessage( "main_GUI-AnimuFrame", status_text=f"Save to: {self.library_type} library",)

    def import_list(self, import_list):
        pass

    def show_library(self):
        """If library not empty, load and display library

        If library is empty, clear listbox (in case search was done beforehand)
        and display message that library is empty

        """
        name_list, library = load.load_library(self.conn, self.library_type, next(self.sort))

        if name_list == None or library == None:
            # Clears the listbox by sending empty list
            pub.sendMessage("populate_listbox", name_list=None)
            pub.sendMessage("main_GUI-AnimuFrame", status_text=f"Nothing in library ({self.library_type}) yet",)
            self.disable_sort = True
            return None

        else:
            self.disable_sort = False
            if not self.in_library:
                self.in_library = True
                self.library_status(next(self.sort))
            self.animu_list = library
            self.name_list = name_list
            pub.sendMessage("populate_listbox", name_list=self.name_list)

    def configure_and_save(self, save_obj, library):
        """Append formatted genre list and full synopsis to animu object and save

        Args:
            save_obj (animu obj): Animu object instance
            library  (string)   : Library type (finished, unfinished, wishlist)
        """
        details = detailed_search(save_obj.mal_id, save_obj.search_type)

        if not details:
            return

        genres = []
        for genre in details["genres"]:
            genres.append(genre["name"])
        genre_string = ", ".join(genres)

        save_obj.synopsis = details["synopsis"]
        save_obj.genre    = genre_string
        save_obj.json     = json.dumps(details)
        save_obj.library  = library

        sql_cmd.insert_data(self.conn, save_obj)

    def save_selected(self):
        """Check if program is in search mode, and if so, save selected anime/manga"""
        if not self.in_library and self.selected_object:
            exists = sql_cmd.check_exists(self.conn, self.selected_object.mal_id)

            if exists:
                pub.sendMessage("main_GUI-AnimuFrame", status_text="Already saved to a library")
                return # If saved already, don't try to save again

            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saving...")
            self.configure_and_save(self.selected_object, self.library_type)
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saved!")

        else:
            pub.sendMessage("main_GUI-AnimuFrame", status_text="No search item selected")

    def delete_selected(self):
        """Delete selection, reload library, clear information section of app"""
        if self.in_library and not (self.selected_index == None):
            mal_id = self.animu_list[self.selected_index].mal_id
            sql_cmd.delete(self.conn, mal_id)

            pub.sendMessage("display_synopsis", synopsis=None)
            pub.sendMessage("display_details",  item_list=None)
            pub.sendMessage("set_webpage",      animu_url=None)
            pub.sendMessage("display_cover",    wx_image=None)
            pub.sendMessage("show_library")

        else:
            pub.sendMessage("main_GUI-AnimuFrame", status_text="No library item selected",)

    def view_selected(self, selected_index):
        """Take selected manga/anime and display its information"""
        self.selected_index = selected_index
        self.selected_object = self.animu_list[selected_index]
        image = wx.Image(BytesIO(self.selected_object.image))

        pub.sendMessage("display_synopsis", synopsis=self.selected_object.synopsis)
        pub.sendMessage("display_details",  item_list=self.selected_object.info_list)
        pub.sendMessage("set_webpage",      animu_url=self.selected_object.url)
        pub.sendMessage("display_cover",    wx_image=image)

    def library_status(self, sort : int):
        """Display current library type and sorting method"""
        sort_messages = [f"Library ({self.library_type}): Unsorted",
                         f"Library ({self.library_type}): Sorted by Name",
                         f"Library ({self.library_type}): Sorted by Type",
                         f"Library ({self.library_type}): Sorted by Name and Type"]
        pub.sendMessage("main_GUI-AnimuFrame", status_text=sort_messages[sort])

    def sort_library(self):
        """Sort current library"""
        
        if self.in_library and not self.disable_sort:
            change_sort_type = self.sort.send # For readability
            change_sort_type(True) # Increment the sorting number for the current library
            sort_type = next(self.sort)

            if sort_type == 0:
                pub.sendMessage("show_library")
                self.library_status(sort_type)

            elif sort_type == 1:
                pub.sendMessage("show_library")
                self.library_status(sort_type)

            elif sort_type == 2:
                pub.sendMessage("show_library")
                self.library_status(sort_type)
                
            elif sort_type == 3:
                pub.sendMessage("show_library")
                self.library_status(sort_type)

            else:
                print("Error with sort function in controller_panel")

            update_config_database(self.conn, self.configs[self.library_type], sort=True)
        else:
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Cannot sort unless in library")
