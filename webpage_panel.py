import theme  # From theme.py
import wx
import webbrowser
from pubsub import pub


class WebpagePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Webpage Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.webpage = None

        self.SetBackgroundColour(theme.background2_dark)

        webpage_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mal_website = wx.Button(self, -1, "MyAnimeList")
        mal_website.Bind(wx.EVT_BUTTON, self.animu_webpage_button)
        webpage_sizer.Add(mal_website, 1, wx.CENTER | wx.EXPAND)

        self.SetSizer(webpage_sizer)

        pub.subscribe(self.set_webpage, "set_webpage")

    def set_webpage(self, animu_url):
        """Set url for webpage button (opens url in browser on button press)"""
        if animu_url:
            self.webpage = animu_url
        else:
            self.webpage = None

    def animu_webpage_button(self, event):
        """If webpage url set for button, open in web browser"""
        if self.webpage:
            webbrowser.open(self.webpage)
        else:
            pub.sendMessage(
                "main_GUI-AnimuFrame", status_text="No anime/manga selected",
            )
