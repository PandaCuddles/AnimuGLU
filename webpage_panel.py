import wx
import webbrowser
from pubsub import pub


class WebpagePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Add Animu Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        webpage_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.webpage = None

        mal_website = wx.Button(self, -1, "MyAnimeList")
        mal_website.Bind(wx.EVT_BUTTON, self.animu_webpage_button)

        webpage_sizer.Add(mal_website, 1, wx.CENTER | wx.EXPAND)

        self.SetSizer(webpage_sizer)

        pub.subscribe(self.set_webpage, "set_webpage")

    def set_webpage(self, animu_url):
        if animu_url:
            self.webpage = animu_url
        else:
            self.webpage = None

    def animu_webpage_button(self, event):
        if self.webpage:
            webbrowser.open(self.webpage)
        else:
            # ? Possibly send "No selection" to status bar when no anime/manga selection has been made
            pass
