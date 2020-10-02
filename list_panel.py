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
        self.animu_list.Bind(wx.EVT_LISTBOX, self.select)

        # Button panel to change library type and sort current library
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Inner sizer for layout reasons
        options_inner = wx.BoxSizer(wx.HORIZONTAL)

        sort_button = wx.Button(self, label="Sort")
        next_button = wx.Button(self, label="Next")

        sort_button.Bind(wx.EVT_BUTTON, self.sort)
        next_button.Bind(wx.EVT_BUTTON, self.next_library)

        options_inner.Add(sort_button, 1, wx.RIGHT | wx.EXPAND, 5)
        options_inner.Add(next_button, 1, wx.EXPAND)

        # Add 20px around list buttons
        options_sizer.Add(options_inner, 1, wx.ALL | wx.EXPAND, 20)

        # Add list box and options box
        list_sizer.Add(self.animu_list, 9, wx.ALL | wx.EXPAND)
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
