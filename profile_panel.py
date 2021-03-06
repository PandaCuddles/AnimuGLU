import sys
import theme  # From theme.py
import webpage_panel
import wx
from pubsub import pub
from wx.lib import statbmp


class ProfilePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Profile Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(theme.background2_dark)
        else:
            self.SetBackgroundColour(theme.background2)

        inner_box = wx.BoxSizer(wx.VERTICAL)
        inner_panel = InnerProfilePanel(self)

        inner_box.Add(inner_panel, 1, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(inner_box)


class InnerProfilePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Inner Profile Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background3_dark)

        profile_box = wx.BoxSizer(wx.VERTICAL)
        profile_image_sizer = wx.BoxSizer(wx.VERTICAL)

        profile_button_format = wx.BoxSizer(wx.VERTICAL)

        profile_pic = ProfileImage(self)
        profile_buttons = ProfileButtons(self)

        profile_image_sizer.Add(
            profile_pic, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 60
        )

        profile_box.Add(profile_image_sizer, 4, wx.BOTTOM | wx.EXPAND, 60)

        # Formats top, and sides of button box
        profile_button_format.Add(
            profile_buttons, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 20
        )
        # Formats bottom of button box
        profile_box.Add(profile_button_format, 5, wx.BOTTOM | wx.EXPAND, 30)
        # profile_box.Add(profile_buttons, 4, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(profile_box)


class ProfileImage(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create Profile Image Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background2_dark)

        # Set profile image after GUI has been initally drawn
        wx.CallLater(0, self.on_resize)

    def on_resize(self):
        bitmap = wx.Bitmap("default.png")

        dimensions = self.GetSize()

        bitmap = self.scale_image(bitmap, dimensions)

        self.Profile = statbmp.GenStaticBitmap(self, wx.ID_ANY, bitmap)
        self.Profile.Center()

    def scale_image(self, bitmap, panel_dimensions):
        # Creates an image frame effect
        width = panel_dimensions[0] - 10
        height = panel_dimensions[1] - 10

        img = bitmap.ConvertToImage()
        img = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)

        new_bitmap = wx.Bitmap(img)

        return new_bitmap


class ProfileButtons(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Format panel for profile panel buttons"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button = Buttons(self)
        button_box.Add(button, 1, wx.TOP | wx.EXPAND, 5)

        self.SetSizer(button_box)


class Buttons(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Buttons panel for profile panel that contains main app buttons"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background3_dark)

        button_sizer = wx.BoxSizer(wx.VERTICAL)

        import_button = wx.Button(self, label="Import")
        #import_button.Bind(wx.EVT_BUTTON, self.import_list)
        button_sizer.Add(import_button, 1, wx.TOP | wx.EXPAND, 5)

        library_button = wx.Button(self, label="Library")
        library_button.Bind(wx.EVT_BUTTON, self.library)
        button_sizer.Add(library_button, 1, wx.TOP | wx.EXPAND, 5)

        delete_button = wx.Button(self, label="Delete")
        delete_button.Bind(wx.EVT_BUTTON, self.delete_animu)
        button_sizer.Add(delete_button, 1, wx.TOP | wx.EXPAND, 5)

        add_button = wx.Button(self, label="Add")
        add_button.Bind(wx.EVT_BUTTON, self.add_animu)
        button_sizer.Add(add_button, 1, wx.TOP | wx.EXPAND, 5)

        exit_button = wx.Button(self, label="Exit")
        exit_button.Bind(wx.EVT_BUTTON, self.exit)
        button_sizer.Add(exit_button, 1, wx.TOP | wx.EXPAND, 5)
        
        self.SetSizer(button_sizer)

    def import_list(self, event):
        # TODO: Add import file text formatting examples to docstring
        """Check import file for item names and content types to add to library
        <put import file formatting examples here>

        """
        import_list = []
        # Base code snippet from here: https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        with wx.FileDialog(
            self,
            "Open import list",
            wildcard="text files (*.txt)|*.txt",
            style=wx.FD_OPEN,
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, "r") as file:
                    file_lines = file.readlines()
                    for line in file_lines:
                        import_list.append(line.replace("\n", ""))
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)
        if len(import_list) > 0:
            pub.sendMessage("import_list", import_list=import_list)

    def library(self, event):
        """Send message to conroller panel to display library contents"""
        pub.sendMessage("show_library")

    def delete_animu(self, event):
        """Send message to controller panel to delete selected item in library"""
        pub.sendMessage("delete_selected")

    def add_animu(self, event):
        """Send message to controller panel to save selected item in search results"""
        pub.sendMessage("save_selected")

    def exit(self, event):
        """Exit application"""
        pub.sendMessage("cleanup")
        sys.exit(0)
