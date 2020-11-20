import theme  # From theme.py
import wx
import jikan_controller
from pubsub import pub


class AnimuSearchPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuSearch Panel

        The search panel consists of a search button, a choice of two search types,
        and a text field to type in the name of the anime/manga you want to search for

        """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.search_btn = wx.Button(self, wx.ID_ANY, label="Search")
        self.search_btn.Bind(wx.EVT_BUTTON, self.search_and_send)
        search_sizer.Add(self.search_btn, 0, wx.RIGHT | wx.CENTER | wx.EXPAND, 3)

        self.search_option = wx.Choice(self, wx.ID_ANY, choices=["Anime", "Manga"])
        self.search_option.SetSelection(0)
        search_sizer.Add(self.search_option, 0, wx.RIGHT | wx.CENTER | wx.EXPAND, 3)

        self.search_text = wx.TextCtrl(self)
        self.search_text.SetBackgroundColour(theme.background3_dark)
        search_sizer.Add(self.search_text, 1, wx.RIGHT | wx.CENTER | wx.EXPAND, 3)

        search_div = wx.BoxSizer(wx.HORIZONTAL)
        search_div.Add(search_sizer, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(search_div)

    def search_and_send(self, event):
        """Jikan search request
        Send non empty search request to jikan backend
        Send search response to list panel for display
        """
        search_type = self.search_option.GetStringSelection()
        search_name = self.search_text.GetValue()

        if search_name == "":
            pub.sendMessage("main_GUI-AnimuFrame", status_text="Nothing to search")
        else:
            name_list, obj_list = jikan_controller.basic_search(search_type, search_name)

            if name_list and obj_list:
                pub.sendMessage(
                    "show_search_results", names=name_list, animu_objects=obj_list
                )
