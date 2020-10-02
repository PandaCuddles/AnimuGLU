import os
import sys
import theme  # From theme.py
import wx
import jikan_controller
from pubsub import pub

image_folder = f"images/"


class AnimuSearchPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuSearch Panel

        Adds Buttons for searching and exiting animuGLU

        """
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # if wx.SystemSettings.GetAppearance().IsDark():
        #    self.SetBackgroundColour(theme.background2_dark)
        # else:
        #    self.SetBackgroundColour(theme.background2)

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        search_btn = wx.Button(self, label="Search")
        search_btn.Bind(wx.EVT_BUTTON, self.search_and_send_animu)

        # exit_btn = wx.Button(self, label="Exit")
        # exit_btn.Bind(wx.EVT_BUTTON, self.exit_animu)

        self.text_input = wx.TextCtrl(self)

        search_type = ["Anime", "Manga"]
        self.animu_choice = wx.Choice(self, choices=search_type)

        self.animu_choice.SetSelection(0)

        # Add selection box for Anime/Manga searches
        search_sizer.Add(search_btn, 0, wx.RIGHT | wx.CENTER, 3)
        search_sizer.Add(self.animu_choice, 0, wx.RIGHT | wx.CENTER, 3)

        # Add input text box for Anime/Manga name and button to exit the program
        search_sizer.Add(self.text_input, 1, wx.RIGHT | wx.CENTER, 3)

        outer_sizer.Add(search_sizer, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(outer_sizer)

    def search_and_send_animu(self, event):
        """Jikan search request
        Send non empty search request to jikan backend
        Send search response to list panel for display
        """
        search_type = self.animu_choice.GetStringSelection()
        search_name = self.text_input.GetValue()

        # ? Possibly add detection of only spaces and skipping search if detected
        if search_name == "":
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="Nothing to search",
            )
        else:
            name_list, obj_list = jikan_controller.basic_search(
                search_type, search_name
            )

            if name_list and obj_list:
                pub.sendMessage(
                    "show_search_results", names=name_list, animu_objects=obj_list
                )

    def exit_animu(self, event):
        """Exit application"""

        # Note: using sys.exit() just raises a SystemExit exception, rather than forcing a program exit

        os._exit(0)
