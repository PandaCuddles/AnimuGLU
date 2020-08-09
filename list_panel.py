import wx
import os
import pickle_unpickle
import dl_thread

from pubsub import pub
from os.path import isfile


class AnimuListPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuList Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(wx.Colour("GREY"))

        list_sizer = wx.BoxSizer()

        """Search results display box"""
        self.animu_list = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.animu_list.Bind(wx.EVT_LISTBOX, self.select)

        list_sizer.Add(self.animu_list, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(list_sizer)

        pub.subscribe(self.populate_listbox, "populate_listbox")

    def populate_listbox(self, name_list):
        if name_list:
            self.animu_list.Clear()  # Clear listbox before populating
            self.animu_list.InsertItems(name_list, 0)  # Insert new search results
        else:
            self.animu_list.Clear()

    # Send the current selection index over to the controller panel
    def select(self, event):
        selection = self.animu_list.GetSelection()

        pub.sendMessage("view_selected", selected_index=selection)

