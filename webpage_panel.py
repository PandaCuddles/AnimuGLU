import wx
import webbrowser
from pubsub import pub


class WebpagePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Add Animu Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(wx.Colour("GREY"))

        webpage_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.webpage = None

        mal_website = wx.Button(self, -1, "MyAnimeList")
        mal_website.Bind(wx.EVT_BUTTON, self.animu_webpage_button)

        webpage_sizer.Add(mal_website, 1, wx.CENTER | wx.EXPAND)

        self.SetSizer(webpage_sizer)

        pub.subscribe(self.current_selection_website, "webpage_panel-WebpagePanel")

    def current_selection_website(self, animu_url):
        self.webpage = animu_url

    def animu_webpage_button(self, event):
        if self.webpage:
            webbrowser.open(self.webpage)
        else:
            # ? Possibly send "No selection" to status bar when no anime/manga selection has been made
            print()