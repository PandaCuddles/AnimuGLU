import wx
import os
import pickle_unpickle
import dl_thread

from pubsub import pub
from os.path import isfile


"""
This panel is an absolute mess!
TODO: Move all the display and image grabbing/library logic into a separate, invisible upper panel...
TODO: ...pubsub information handling only works within the wx.app process (breaks if done within an outside standalone function)
"""


class AnimuListPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuList Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(wx.Colour("GREY"))

        list_sizer = wx.BoxSizer()

        """Search results display box"""
        self.animu_list = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.animu_list.Bind(wx.EVT_LISTBOX, self.view_curr_selection)

        list_sizer.Add(self.animu_list, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(list_sizer)

        self.animu_objects = None

        self.curr_thread = False

        self.in_library = False

        self.image_list = None

        """Listener for search results"""
        pub.subscribe(self.search_results, "list_panel_listener")
        pub.subscribe(self.ListLibrary, "list_panel-Library")
        pub.subscribe(self.DeleteSelected, "list_panel-Delete")

    def search_results(self, names, animu_objects):
        """Display anime/manga info

        Populate list box and download cover images

        Stop downloads for previous search if active

        Download cover images for new search

        """
        self.in_library = False
        self.animu_objects = animu_objects
        self.animu_list.Clear()  # Clear listbox before populating
        self.animu_list.InsertItems(names, 0)  # Insert new search results

        if self.curr_thread and self.curr_thread.is_alive:
            self.curr_thread.KILL = True
            self.curr_thread.join()

        self.curr_thread = dl_thread.DownloadThread(search_list=animu_objects)

        self.curr_thread.start()

    def view_curr_selection(self, event):
        if not self.in_library:
            item_index = self.animu_list.GetSelection()
            selected_animu = self.animu_objects[item_index]

            synopsis = selected_animu.synopsis
            url = selected_animu.image_url
            self.path = selected_animu.localImage

            self.dl_object = self.animu_objects[item_index]
            self.path = self.animu_objects[item_index].localImage

            # Send synopsis to synopsis box
            pub.sendMessage("info_panel-SynopsisPanel", synopsis=synopsis)

            # Send data to detail_box
            pub.sendMessage("info_panel-DetailList", item_list=self.dl_object.info_list)

            # Send MAL animu url to website button thingy
            pub.sendMessage("webpage_panel-WebpagePanel", animu_url=selected_animu.url)

            # Saves the selected anime if the add button is pressed
            pub.subscribe(self.SaveAnimu, "list_panel-AnimuListPanel")

            # Checks for image file before drawing image
            self.exists = isfile(self.path)

            if self.exists:
                self.send_draw_request()
        elif self.in_library:
            index = self.animu_list.GetSelection()
            img = self.animu_objects[index][0]
            animu = self.animu_objects[index][1]
            pub.sendMessage("image_panel-ImageDisplay", wx_image=img)
            pub.sendMessage("info_panel-SynopsisPanel", synopsis=animu.synopsis)
            pub.sendMessage("info_panel-DetailList", item_list=animu.info_list)
            pub.sendMessage("webpage_panel-WebpagePanel", animu_url=animu.url)
        else:
            print("Ya dead, son")

    def send_draw_request(self):
        draw_image = wx.Image(self.path, wx.BITMAP_TYPE_ANY)
        pub.sendMessage("image_panel-ImageDisplay", wx_image=draw_image)

    def SaveAnimu(self):

        pub.sendMessage("main_GUI-AnimuFrame", status_text="Saving animu...")

        if self.exists:
            pickle_unpickle.pickle_save(self.dl_object, self.path)
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Done")
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame",
                status_text="Cover image not downloaded, please wait...",
            )

    def ListLibrary(self, name_list, animu_tuple_list):
        self.in_library = True
        self.animu_list.Clear()  # Clear listbox before populating
        self.animu_list.InsertItems(name_list, 0)
        self.animu_objects = animu_tuple_list
        pub.sendMessage(
            "main_GUI-AnimuFrame", status_text="Library",
        )

    def DeleteSelected(self):
        if self.in_library:

            index = self.animu_list.GetSelection()
            animu = self.animu_objects[index][1]
            default_path = f"{os.getcwd()}/saved/"
            id_to_delete = f"{str(animu.mal_id)}.pkl"

            os.remove(f"{default_path}{id_to_delete}")

            names, animu_list = pickle_unpickle.load_library()

            if names == None and animu_list == None:
                self.animu_list.Clear()
                pub.sendMessage(
                    "main_GUI-AnimuFrame", status_text="Nothing in library yet"
                )
                return
            else:
                pub.sendMessage(
                    "list_panel-Library", name_list=names, animu_tuple_list=animu_list,
                )
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="No library item selected",
            )
