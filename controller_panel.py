import wx
import jikan_controller
import dl_thread
import pickle_unpickle

from pubsub import pub
from os import remove
from os.path import isfile

base_path = "saved/"

# TODO: Redo Controller Panel docstring
class ControllerPanel(wx.Panel):
    """Controller Panel containing key program logic, and acts as a 'main hub' for different parts of the program"""

    def __init__(self, parent, *args, **kwargs):

        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.just_soup = "there's only soup"
        self.soup = "get out of the soup isle"

        self.current_animu_list = None
        self.library_image_list = None
        self.curr_thread = False

        self.in_library = False

        self.image_list = None
        self.image_path = None
        self.image_exists = None

        self.selected_object = None
        self.selected_index = None

        pub.subscribe(self.show_search_results, "show_search_results")
        pub.subscribe(self.show_library, "show_library")
        pub.subscribe(self.delete_selected, "delete_selected")
        pub.subscribe(self.save_selected, "save_selected")
        pub.subscribe(self.view_selected, "view_selected")
        pub.subscribe(self.import_list, "import_list")

    def show_search_results(self, names, animu_objects):
        """ Send results to listbox and download cover images

        Args:
            animu_objects : [obj1, obj2, obj3]

            names : ["name1", "name2", "name3"]

        """
        self.in_library = False
        self.current_animu_list = animu_objects
        pub.sendMessage("populate_listbox", name_list=names)
        self.download_cover_images(animu_objects)

    def download_cover_images(self, search_results):
        """Download cover images from list of search results

        Args:
            search_results (list): list of animu objects

            e.g. [animu_obj1, animu_obj2, animu_obj3, etc.]

        """

        if self.curr_thread and self.curr_thread.is_alive:
            self.curr_thread.KILL = True
            self.curr_thread.join()

        self.curr_thread = dl_thread.DownloadThread(search_list=search_results)
        self.curr_thread.start()

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
        # for item in formatted_import_list:
        #    print(item)
        # TODO: Send list to a custom download function for info + PIL img
        # TODO: Loop through items and send each one to the pickle function

    def show_library(self):

        name_list, library_objects, library_images = pickle_unpickle.load_library()

        if name_list == None or library_objects == None:
            pub.sendMessage("populate_listbox", name_list=name_list)
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Nothing in library yet")
            self.in_library = False
            return
        else:
            self.in_library = True

            self.library_image_list = library_images
            self.current_animu_list = library_objects

            pub.sendMessage("populate_listbox", name_list=name_list)
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="Library",
            )

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

    def save_selected(self):
        """Check if program is in search mode, and if so, save selected anime/manga"""
        if not self.in_library and self.selected_object:
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saving...")

            # Retrieve more detailed info on selected item
            expanded_details = jikan_controller.detailed_search(
                self.selected_object.mal_id, self.selected_object.searchType
            )
            # Add extra details to animu object before pickling
            self.configure_save(self.selected_object, expanded_details)

            pickle_unpickle.pickle_save(
                self.selected_object, self.selected_object.localImage
            )

            pub.sendMessage("main_GUI-AnimuFrame", status_text="Saved!")
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="No search item selected"
            )

    def delete_selected(self):
        if self.in_library:

            animu = self.current_animu_list[self.selected_index]

            remove(f"{base_path}{str(animu.mal_id)}.pkl")
            pub.sendMessage("show_library")
            pub.sendMessage("display_synopsis", synopsis=None)
            pub.sendMessage("display_details", item_list=None)
            pub.sendMessage("set_webpage", animu_url=None)
            pub.sendMessage("display_cover", wx_image=None)

        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="No library item selected",
            )

    def view_selected(self, selected_index):
        self.selected_index = selected_index
        self.selected_object = self.current_animu_list[selected_index]

        if not self.in_library:
            pub.sendMessage("display_synopsis", synopsis=self.selected_object.synopsis)
            pub.sendMessage("display_details", item_list=self.selected_object.info_list)
            pub.sendMessage("set_webpage", animu_url=self.selected_object.url)
            self.image_exists = isfile(self.selected_object.localImage)

            if self.image_exists:
                wx_image = wx.Image(self.selected_object.localImage, wx.BITMAP_TYPE_ANY)
                pub.sendMessage("display_cover", wx_image=wx_image)

        elif self.in_library:
            pub.sendMessage("display_synopsis", synopsis=self.selected_object.synopsis)
            pub.sendMessage("display_details", item_list=self.selected_object.info_list)
            pub.sendMessage("set_webpage", animu_url=self.selected_object.url)
            pub.sendMessage(
                "display_cover", wx_image=self.library_image_list[selected_index]
            )
        else:
            print("Ya dead, son")

