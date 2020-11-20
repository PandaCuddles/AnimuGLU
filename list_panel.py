import theme  # From theme.py
import wx

from pubsub import pub


class AnimuListPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuList Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background3_dark)

        list_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create listbox to display anime/manga titles for both search results and library results
        self.animu_list = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)

        # Test
        self.animu_list.SetBackgroundColour(theme.background3_dark)

        self.animu_list.Bind(wx.EVT_LISTBOX, self.select)
        list_sizer.Add(self.animu_list, 9, wx.ALL | wx.EXPAND)

        options_div = wx.BoxSizer(wx.HORIZONTAL)
        sort_button = wx.Button(self, label="Sort")
        sort_button.Bind(wx.EVT_BUTTON, self.sort)
        options_div.Add(sort_button, 1, wx.RIGHT | wx.EXPAND, 5)

        next_button = wx.Button(self, label="Next")
        next_button.Bind(wx.EVT_BUTTON, self.next_library)
        options_div.Add(next_button, 1, wx.EXPAND)

        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        options_sizer.Add(options_div, 1, wx.ALL | wx.EXPAND, 20)
        list_sizer.Add(options_sizer, 1, wx.EXPAND)

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

    def sort(self, event):
        """Sort current listing if in library"""
        pub.sendMessage("sort_library")

    def next_library(self, event):
        """Display the next library type if available"""
        pub.sendMessage("next_library")
