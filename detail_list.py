import theme
import wx
import wx.lib.agw.ultimatelistctrl as ULC

from dateutil import parser
from pubsub import pub



class DetailsPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        """Create the Details Panel"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.initUI()
    
    def initUI(self):
        self.SetBackgroundColour(theme.background3_dark)
        detail_sizer = wx.BoxSizer(wx.VERTICAL)
        self.detailList = DetailList(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES,) # List control object
        detail_sizer.Add(self.detailList, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(detail_sizer)


#class DetailList(wx.ListCtrl):
class DetailList(ULC.UltimateListCtrl):
    def __init__(self, parent, *args, **kwargs):
        """Create the Detail List Panel"""
        #wx.ListCtrl.__init__(self, parent, *args, **kwargs)
        super().__init__(parent, wx.ID_ANY, agwStyle=ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_ALIGN_LEFT | ULC.ULC_NO_HIGHLIGHT | ULC.ULC_VRULES | ULC.ULC_HRULES)
        super().SetBackgroundColour(theme.background3_dark)

        self.parent = parent
        
        self.initUI()

        pub.subscribe(self.display_details, "display_details")

    def initUI(self):
        self.SetBackgroundColour(theme.background3_dark)
        self.InsertColumn(0, "Details", format=ULC.ULC_FORMAT_LEFT, width=-1)
        self.InsertColumn(1, "", format=ULC.ULC_FORMAT_LEFT, width=-1)

    def display_details(self, item_list : list):
        """Display anime/manga information, (e.g. name, rating, start/end date)

        Args:
            item_list (list): contains list of tuples, each an anime/manga detail (e.g. (Name, SomeName))
        """

        # wx List Control boxes can take in tuples as input
        # and autofill each column with the tuple contents
        if item_list:
            self.DeleteAllItems()

            for item in item_list:
                i = self.format_item(item)
                self.Append(i)

            # Resize columns to fit largest string in each column
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        else:
            self.DeleteAllItems()

    def format_item(self, item):
        """format anime/manga details (e.g. Airing date into human readable format)

        Args:
            item (tuple): detail name and detail info

        Returns:
            tuple: formatted detail name and detail info converted to string
        """

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
            # Sends the details into the corresponding function to be formatted
            formatted = formatter[item[0]](item[1])
            return (self.name(item[0]), formatted)  # Formats name, if needed

        else:
            return (item[0], str(item[1]))

    def airing(self, airing):
        """Returns Airing value as a string, unless None, which will return 'No', as formatted on MAL"""
        if airing:
            return str(airing)
        else:
            return "No"

    def format_date(self, date):
        """Turns date string into a human readable format"""
        if date:
            parsed = parser.parse(date)

            month = parsed.strftime("%b")
            day = str(parsed.day)
            year = str(parsed.year)

            return f"{month} {day}, {year}"
        else:
            return "?"

    def publishing(self, publishing):
        """Converts publishing value from a boolean into a correctly formatted name, as formatted on MAL"""
        if publishing:
            return "Publishing"
        else:
            return "Finished"

    def has_chpt_vol(self, chpt_vol):
        """Returns Chapter Volume as a string, unless None, which will return 'Unknown', as formatted on MAL"""
        if chpt_vol:
            return str(chpt_vol)
        else:
            return "Unknown"

    def score(self, score):
        """Score of 0 returns string 'None', as displayed on MAL (otherwise returns score as a string)"""
        if score == 0:
            return "None"
        else:
            return str(score)

    def name(self, name):
        """Formats Publishing status name, since jikan API returns 'Publishing' as the detail name,
           rather than 'Status' (MAL displays detail as 'Status')"""
        if name == "Publishing":
            return "Status"
        else:
            return name
