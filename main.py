#!/usr/bin/env python3.7

"""

Requires: pypubsub

"""
import wx
import animu_panel
import list_panel
import search_panel
import controller_panel

from pubsub import pub


class MainPanelSubTop(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Main Top Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.Colour("DARK ORANGE"))
        else:
            self.SetBackgroundColour(wx.Colour("ORANGE"))

        """Split the top panel left/right into two sections"""
        animu_sizer = wx.BoxSizer(wx.HORIZONTAL)
        animu_sizer.Add(list_panel.AnimuListPanel(self), 1, wx.RIGHT | wx.EXPAND, 5)
        animu_sizer.Add(animu_panel.AnimuPanel(self), 3, wx.LEFT | wx.EXPAND, 5)
        self.SetSizer(animu_sizer)


class MainPanelSubBottom(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Main Bottom Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        """Split the bottom panel left/right into two sections"""
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(search_panel.AnimuSearchPanel(self), 1, wx.EXPAND)

        self.SetSizer(search_sizer)


class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Search Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.Colour("DARK ORANGE"))
        else:
            self.SetBackgroundColour(wx.Colour("ORANGE"))

        main_controller = controller_panel.ControllerPanel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(
            MainPanelSubTop(self), 9, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 10
        )
        main_sizer.Add(MainPanelSubBottom(self), 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(main_sizer)


class AnimuFrame(wx.Frame):
    """Main Frame holding the Panel."""

    def __init__(self, *args, **kwargs):
        """Create the  Main Panel within the Main Frame"""
        wx.Frame.__init__(self, *args, **kwargs)

        main_panel = MainPanel(self)

        """Status Bar for updates"""
        self.status_bar = self.CreateStatusBar(
            style=wx.STB_DEFAULT_STYLE ^ wx.STB_SIZEGRIP,
        )
        if wx.SystemSettings.GetAppearance().IsDark():
            self.status_bar.SetBackgroundColour(wx.Colour("DARK ORANGE"))
        else:
            self.status_bar.SetBackgroundColour(wx.Colour("ORANGE"))
        self.status_bar.SetStatusText("  Welcome to AnimuGLU!")
        self.status_bar.SetStatusStyles([wx.SB_RAISED])

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        pub.subscribe(self.update_status_bar, "main_GUI-AnimuFrame")

    def update_status_bar(self, status_text):
        """Update status bar

        Args:
            status_text (String): New status for AnimuGLU
        """
        self.status_bar.SetStatusText(status_text)


if __name__ == "__main__":
    app = wx.App(False)

    frame = AnimuFrame(
        None,
        wx.ID_ANY,
        "AnimuGLU Alpha v0.5",
        size=(1280, 720),
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
    )

    frame.Show(True)
    app.MainLoop()
