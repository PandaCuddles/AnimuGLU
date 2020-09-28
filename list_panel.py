import theme  # From theme.py
import wx

from pubsub import pub


class AnimuListPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuList Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background2)

        list_sizer = wx.BoxSizer()

        self.animu_list = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.animu_list.Bind(wx.EVT_LISTBOX, self.select)

        list_sizer.Add(self.animu_list, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(list_sizer)

        pub.subscribe(self.populate_listbox, "populate_listbox")

    def populate_listbox(self, name_list):
        """Clear list box if empty, or clear listbox and repopulate if not empty"""
        if name_list:
            self.animu_list.Clear()
            self.animu_list.InsertItems(name_list, 0)
        else:
            self.animu_list.Clear()

    def select(self, event):
        """Send the current selection index over to the controller panel"""
        selection = self.animu_list.GetSelection()

        pub.sendMessage("view_selected", selected_index=selection)
