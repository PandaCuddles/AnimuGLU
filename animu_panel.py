import credits_panel
import info_panel
import profile_panel
import wx


class AnimuPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Only works for platforms that support transparency
        if self.CanSetTransparent:
            self.SetTransparent(100)

        info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        profile_box = wx.BoxSizer(wx.VERTICAL)

        profile = profile_panel.ProfilePanel(self)
        animuGLU_credits = credits_panel.CreditsPanel(self)

        profile_box.Add(profile, 4, wx.BOTTOM | wx.EXPAND, 5)
        profile_box.Add(animuGLU_credits, 1, wx.TOP | wx.EXPAND, 5)

        info_box = info_panel.AnimuInfoPanel(self)

        info_sizer.Add(info_box, 2, wx.EXPAND)
        info_sizer.Add(profile_box, 1, wx.LEFT | wx.EXPAND, 10)

        self.SetSizer(info_sizer)
