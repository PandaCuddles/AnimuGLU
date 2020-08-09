import wx


class CreditTextPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Credit Text Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.Colour("WHITE"))

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        text_sizer = wx.BoxSizer(wx.VERTICAL)

        credits_title = wx.StaticText(self, label="Credits", style=wx.ALIGN_CENTER)
        credits_text = wx.StaticText(
            self, label="Developer: PandaCuddles", style=wx.ALIGN_CENTER,
        )

        text_sizer.Add(credits_title, 0, wx.ALL | wx.EXPAND, 5)
        text_sizer.Add(credits_text, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(text_sizer)


class CreditsPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Credits Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        credits_sizer = wx.BoxSizer(wx.VERTICAL)

        credits_panel = CreditTextPanel(self)

        credits_sizer.Add(credits_panel, 1, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(credits_sizer)
