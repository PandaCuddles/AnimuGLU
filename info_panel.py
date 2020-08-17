import wx
import webpage_panel

from wx.lib import statbmp
from pubsub import pub
from dateutil import parser


class AnimuInfoPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Info Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        info_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        top_section_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_section_sizer = wx.BoxSizer(wx.VERTICAL)

        image_panel = ImagePanel(self)
        animu_details_panel = DetailsPanel(self)
        top_section_sizer.Add(image_panel, 7, wx.EXPAND)
        top_section_sizer.Add(animu_details_panel, 13, wx.LEFT | wx.EXPAND, 10)

        synopsis_panel = SynopsisPanel(self)
        bottom_section_sizer.Add(
            synopsis_panel, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND, 20
        )

        info_panel_sizer.Add(
            top_section_sizer, 4, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 20
        )
        info_panel_sizer.Add(bottom_section_sizer, 3, wx.TOP | wx.EXPAND, 10)

        self.SetSizer(info_panel_sizer)


class SynopsisPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.WHITE)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        synopsis_sizer = wx.BoxSizer(wx.VERTICAL)
        synopsis_title = wx.StaticText(self, label="Synopsis:")
        self.synopsis_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        synopsis_sizer.Add(synopsis_title, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        synopsis_sizer.Add(
            self.synopsis_text, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5
        )

        self.SetSizer(synopsis_sizer)

        pub.subscribe(self.display_synopsis, "display_synopsis")

    def display_synopsis(self, synopsis):
        """Display synopsis

        Args:
            synopsis (String): Synopsis of the currently selected anime/manga
        """
        if synopsis:
            self.synopsis_text.Clear()
            self.synopsis_text.SetValue(synopsis)
        else:
            self.synopsis_text.Clear()


class DetailsPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.WHITE)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        detail_sizer = wx.BoxSizer(wx.VERTICAL)

        """List control object"""
        self.detailList = DetailList(
            self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES,
        )

        detail_sizer.Add(self.detailList, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(detail_sizer)


class DetailList(wx.ListCtrl):
    def __init__(self, parent, *args, **kwargs):
        wx.ListCtrl.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.InsertColumn(0, "Details", wx.LIST_FORMAT_LEFT, width=-1)
        self.index_data = self.InsertColumn(1, "", wx.LIST_FORMAT_LEFT, width=-1)

        self.SetColumnWidth(1, -3)

        pub.subscribe(self.display_details, "display_details")

    def display_details(self, item_list):
        if item_list:
            self.DeleteAllItems()

            for item in item_list:

                i = self.format_item(item)

                self.Append(i)

            self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        else:
            self.DeleteAllItems()

    def format_item(self, item):

        formatter = {
            "Airing": self.airing,
            "Start Date": self.format_date,
            "End Date": self.format_date,
            "Publishing": self.publishing,
            "Chapters": self.has_chpt_vol,
            "Volumes": self.has_chpt_vol,
            "Score": self.score,
        }

        if item[0] in formatter:
            "Sends the details into the corresponding function to be formatted"
            formatted = formatter[item[0]](item[1])
            return (self.name(item[0]), formatted)  # Formats name, if needed

        else:
            return (item[0], str(item[1]))

    def airing(self, airing):
        if airing:
            return str(airing)
        else:
            return "No"

    def format_date(self, date):
        if date:
            parsed = parser.parse(date)

            month = parsed.strftime("%b")
            day = str(parsed.day)
            year = str(parsed.year)

            return f"{month} {day}, {year}"
        else:
            return "?"

    def publishing(self, publishing):
        if publishing:
            return "Publishing"
        else:
            return "Finished"
        i = ("Status", "Publishing")

    def has_chpt_vol(self, chpt_vol):
        if chpt_vol:
            return str(chpt_vol)
        else:
            return "Unknown"

    def score(self, score):
        if score == 0:
            return "None"
        else:
            return str(score)

    def name(self, name):
        if name == "Publishing":
            return "Status"
        else:
            return name


class ImagePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Animu Text Info Panel"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        if wx.SystemSettings.GetAppearance().IsDark():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(19))
        else:
            self.SetBackgroundColour(wx.Colour("GREY"))

        sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer_ext = wx.BoxSizer(wx.HORIZONTAL)

        image = ImageDisplay(self)
        webpage_button = webpage_panel.WebpagePanel(self)
        button_sizer.Add(webpage_button, 1, wx.TOP | wx.EXPAND, 10)
        button_sizer_ext.Add(button_sizer, 1, wx.BOTTOM | wx.EXPAND)

        sizer.Add(image, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND)
        sizer.Add(button_sizer_ext, 0, wx.LEFT | wx.RIGHT | wx.EXPAND)

        self.SetSizer(sizer)


class ImageDisplay(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # self.SetBackgroundColour(wx.Colour("WHITE"))

        self.SetBackgroundColour(wx.SystemSettings.GetColour(4))

        """If an anime/manga is clicked on in the list section"""
        pub.subscribe(self.display_cover, "display_cover")

        self.Bind(wx.EVT_SIZE, self.on_resize)

        self.image = False

        self.ImgCover = None

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

