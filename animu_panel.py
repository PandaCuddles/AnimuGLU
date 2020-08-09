import wx

import credits_panel
import info_panel
import profile_panel


class AnimuPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the AnimuInfo Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.Colour("DARK ORANGE"))
        else:
            self.SetBackgroundColour(wx.Colour("ORANGE"))

        info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        profile_box = wx.BoxSizer(wx.VERTICAL)

        """Panels for profile and credits"""
        profile = profile_panel.ProfilePanel(self)
        animuGLU_credits = credits_panel.CreditsPanel(self)

        profile_box.Add(profile, 4, wx.BOTTOM | wx.EXPAND, 5)
        profile_box.Add(animuGLU_credits, 1, wx.TOP | wx.EXPAND, 5)

        """Right side of the anime info section with the info boxes"""
        info_box = info_panel.AnimuInfoPanel(self)

        """Add both the image section and text section to the info panel"""
        info_sizer.Add(info_box, 2, wx.EXPAND)
        info_sizer.Add(profile_box, 1, wx.LEFT | wx.EXPAND, 10)

        self.SetSizer(info_sizer)

