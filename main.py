#!/usr/bin/env python3.8

import animu_panel
import controller_panel
import jikan_controller
import list_panel
import search_panel
import sql_cmd

import os
import wx

from pubsub import pub


class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Search Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(wx.Colour("DARK ORANGE"))

        self.initUI()

    def initUI(self):
        # Initialize controller panel, creating the hub for pub/sub communications
        controller_panel.ControllerPanel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Split the top section left/right into two sections
        animu_sizer = wx.BoxSizer(wx.HORIZONTAL)
        animu_sizer.Add(list_panel.AnimuListPanel(self), 1, wx.RIGHT | wx.EXPAND, 5)
        animu_sizer.Add(animu_panel.AnimuPanel(self), 3, wx.LEFT | wx.EXPAND, 5)

        # Setup bottom section with the search panel
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(search_panel.AnimuSearchPanel(self), 1, wx.EXPAND)

        main_sizer.Add(search_sizer, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(animu_sizer, 11, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        self.SetSizer(main_sizer)


class AnimuFrame(wx.Frame):
    """Main Frame holding the Panel."""

    def __init__(self, *args, **kwargs):
        """Create the  Main Panel within the Main Frame"""
        super().__init__(*args, **kwargs)

        # Exit app if another app was started already
        self.name = f"AnimuGLU-{wx.GetUserId()}"
        self.instance = wx.SingleInstanceChecker(self.name)

        # Keeps only one instance of the app running at a time
        if self.instance.IsAnotherRunning():
            wx.MessageBox("App is already running", "ERROR")
            os._exit(0)

        self.initUI()

        pub.subscribe(self.update_status_bar, "main_GUI-AnimuFrame")
    
    def initUI(self):
        
        self.main_panel = MainPanel(self)

        # Status Bar for updates
        self.status_bar = self.CreateStatusBar(style=wx.STB_DEFAULT_STYLE ^ wx.STB_SIZEGRIP)

        # Set initial status bar text
        self.status_bar.SetStatusText("Welcome to AnimuGLU!")
        self.status_bar.SetStatusStyles([wx.SB_RAISED])

        if wx.SystemSettings.GetAppearance().IsDark():
            self.status_bar.SetBackgroundColour(wx.Colour("DARK ORANGE"))
            self.status_bar.SetForegroundColour(wx.Colour("BLACK")) # Sets text color to black
        else:
            self.status_bar.SetBackgroundColour(wx.Colour("ORANGE"))
            self.status_bar.SetForegroundColour(wx.Colour("WHITE")) # Sets text color to white

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def update_status_bar(self, status_text):
        """Update status bar

        Args:
            status_text (String): New status for AnimuGLU
        """
        self.status_bar.SetStatusText(status_text)


if __name__ == "__main__":

    if not os.path.isfile("animu.db"):
        conn = sql_cmd.setup()
        sql_cmd.create_data_table(conn)
        sql_cmd.create_config_table(conn)
        sql_cmd.default_config(conn)
        conn.close()
        print("(setup) Database connection closed")

    app = wx.App(False)

    frame = AnimuFrame(
        None,
        wx.ID_ANY,
        "AnimuGLU Alpha v0.7",
        size=(1280, 720),
        # style=wx.DEFAULT_FRAME_STYLE,
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,  # Prevent window resizing
    )

    frame.Show(True)
    app.MainLoop()
