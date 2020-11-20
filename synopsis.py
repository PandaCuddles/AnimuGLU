import theme
import wx

from pubsub import pub


class SynopsisPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Synopsys Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background3_dark)

        synopsis_sizer = wx.BoxSizer(wx.VERTICAL)
        synopsis_title = wx.StaticText(self, label="Synopsis:")
        synopsis_sizer.Add(synopsis_title, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        self.synopsis_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.synopsis_text.SetBackgroundColour(theme.background3_dark)
        synopsis_sizer.Add(self.synopsis_text, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        self.SetSizer(synopsis_sizer)

        pub.subscribe(self.display_synopsis, "display_synopsis")

    def display_synopsis(self, synopsis):

        """Display synopsis

        Args:
            synopsis (String): Synopsis of the currently selected anime/manga
        """
        if synopsis:
            self.synopsis_text.Clear()
            self.synopsis_text.SetValue(synopsis)
        else:
            self.synopsis_text.Clear()