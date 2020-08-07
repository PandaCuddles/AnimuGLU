import os
import sys
import wx
import jikan_controller
from pubsub import pub


class AnimuSearchPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuSearch Panel

        Adds Buttons for searching and exiting animuGLU

        """
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(wx.Colour("GREY"))

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)

        search_btn = wx.Button(self, label="Search")
        search_btn.Bind(wx.EVT_BUTTON, self.search_and_send_animu)

        exit_btn = wx.Button(self, label="Exit")
        exit_btn.Bind(wx.EVT_BUTTON, self.exit_animu)

        self.text_input = wx.TextCtrl(self)

        search_type = ["Anime", "Manga"]
        self.animu_choice = wx.Choice(self, choices=search_type)

        self.animu_choice.SetSelection(0)

        search_sizer.Add(self.animu_choice, 0, wx.ALL | wx.CENTER, 3)
        search_sizer.Add(search_btn, 0, wx.ALL | wx.CENTER, 3)
        search_sizer.Add(self.text_input, 1, wx.ALL | wx.CENTER, 3)
        search_sizer.Add(exit_btn, 0, wx.ALL | wx.CENTER, 3)

        self.SetSizer(search_sizer)

    def search_and_send_animu(self, event):
        """Jikan search request
        Send search request to jikan backend
        Send search response to list panel for display
        Default search to a space if the search box was empty on clicking search
        """
        search_type = self.animu_choice.GetStringSelection()
        search_name = self.text_input.GetValue()

        if search_name == "":
            search_name = " "

        name_list, obj_list = jikan_controller.basic_search(search_type, search_name)

        pub.sendMessage("show_search_results", names=name_list, animu_objects=obj_list)

    def exit_animu(self, event):
        """Exit application

        Note to self: sys.exit() just raises a SystemExit exception
        inside the current thread, it doesn't actually force the program
        closed.

        """
        os._exit(1)
        # sys.exit()
        pass
