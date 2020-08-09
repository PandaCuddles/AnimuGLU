import wx
import pickle_unpickle
import webpage_panel
import licenses_popup

from pubsub import pub
from wx.lib import statbmp


class ProfilePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Text Info Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        inner_box = wx.BoxSizer(wx.VERTICAL)
        inner_panel = InnerProfilePanel(self)

        inner_box.Add(inner_panel, 1, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(inner_box)


class InnerProfilePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Text Info Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.Colour("WHITE"))

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        profile_box = wx.BoxSizer(wx.VERTICAL)
        profile_image_sizer = wx.BoxSizer(wx.VERTICAL)

        profile_pic = ProfileImage(self)
        profile_buttons = ProfileButtons(self)

        profile_image_sizer.Add(
            profile_pic, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 60
        )

        profile_box.Add(profile_image_sizer, 5, wx.BOTTOM | wx.EXPAND, 45)
        profile_box.Add(profile_buttons, 4, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(profile_box)


class ProfileImage(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        bitmap = wx.Bitmap("default.png")

        dimensions = event.GetSize()

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
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        button_box = wx.BoxSizer(wx.HORIZONTAL)

        button = Buttons(self)

        button_box.Add(button, 1, wx.TOP | wx.EXPAND, 5)

        self.SetSizer(button_box)


# TODO: Add Import button and import functionality
class Buttons(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.Colour("WHITE"))

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        button_sizer = wx.BoxSizer(wx.VERTICAL)

        license_button = wx.Button(self, label="Licenses")

        library_button = wx.Button(self, label="Library")

        delete_button = wx.Button(self, label="Delete")

        add_button = wx.Button(self, label="Add")

        license_button.Bind(wx.EVT_BUTTON, self.show_license)
        library_button.Bind(wx.EVT_BUTTON, self.library)
        delete_button.Bind(wx.EVT_BUTTON, self.delete_animu)
        add_button.Bind(wx.EVT_BUTTON, self.add_animu)

        button_sizer.Add(license_button, 1, wx.TOP | wx.EXPAND, 5)
        button_sizer.Add(library_button, 1, wx.TOP | wx.EXPAND, 5)
        button_sizer.Add(delete_button, 1, wx.TOP | wx.EXPAND, 5)
        button_sizer.Add(add_button, 1, wx.TOP | wx.EXPAND, 5)

        self.SetSizer(button_sizer)

    def show_license(self, event):
        dialogue = licenses_popup.LicensesPopup(self, title="Licenses", size=(250, 250))
        dialogue.Show(True)

    def library(self, event):
        pub.sendMessage("show_library")

    def delete_animu(self, event):
        pub.sendMessage("delete_selected")

    def add_animu(self, event):
        pub.sendMessage("save_selected")
