import theme  # From theme.py
import webpage_panel
import wx

from pubsub import pub
from wx.lib import statbmp

from detail_list import DetailsPanel
from synopsis import SynopsisPanel


class AnimuInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Panel containing the anime/manga cover image, details, and synopsis"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.SetBackgroundColour(theme.background2_dark)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_panel = ImagePanel(self)
        top_sizer.Add(image_panel, 7, wx.EXPAND)

        details_panel = DetailsPanel(self)
        top_sizer.Add(details_panel, 13, wx.LEFT | wx.EXPAND, 10)

        bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        synopsis_panel = SynopsisPanel(self)
        bottom_sizer.Add(synopsis_panel, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND, 20)

        info_sizer = wx.BoxSizer(wx.VERTICAL)
        info_sizer.Add(top_sizer, 4, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 20)
        info_sizer.Add(bottom_sizer, 3, wx.TOP | wx.EXPAND, 10)

        self.SetSizer(info_sizer)


class ImagePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Text Info Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.SetBackgroundColour(theme.background2_dark)

        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_panel = ImageDisplay(self)
        image_sizer.Add(image_panel, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND)
        
        mal_div = wx.BoxSizer(wx.HORIZONTAL)
        webpage_button = webpage_panel.WebpagePanel(self)
        mal_div.Add(webpage_button, 1, wx.TOP | wx.EXPAND, 10)


        mal_sizer= wx.BoxSizer(wx.HORIZONTAL)
        mal_sizer.Add(mal_div, 1, wx.BOTTOM | wx.EXPAND)
        image_sizer.Add(mal_sizer, 0, wx.LEFT | wx.RIGHT | wx.EXPAND)

        self.SetSizer(image_sizer)


class ImageDisplay(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Panel that will display the anime/manga cover image"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.image = False
        self.ImgCover = None

        self.SetBackgroundColour(theme.background3_dark)

        #If an anime/manga is clicked on in the list section
        pub.subscribe(self.display_cover, "display_cover")


    def display_cover(self, wx_image):
        """Resize and display cover image

        Args:
            wx_image (wx.Image object): local image file turned into a wx.Image object
        """
        if wx_image:
            self.image = wx_image

            panel_dimensions = self.GetSize()

            bitmap = wx.Bitmap(self.image)

            scaled_bitmap = self.scale_image(bitmap, panel_dimensions)

            if self.ImgCover:
                self.ImgCover.Destroy()

            self.ImgCover = statbmp.GenStaticBitmap(self, wx.ID_ANY, scaled_bitmap)
            self.ImgCover.Center()

        else:  # Reset info panel when deleting library item
            if self.ImgCover:
                self.ImgCover.Destroy()

    def on_resize(self, event):
        if self.image:

            dimensions = event.GetSize()
            bitmap = wx.Bitmap(self.image)
            bitmap = self.scale_image(bitmap, dimensions)

            self.ImgCover = statbmp.GenStaticBitmap(self, wx.ID_ANY, bitmap)
            self.ImgCover.Center()

    def scale_image(self, bitmap, panel_dimensions):
        width = panel_dimensions[0]
        height = panel_dimensions[1]

        img = bitmap.ConvertToImage()
        img = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        new_bitmap = wx.Bitmap(img)

        return new_bitmap
