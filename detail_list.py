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
                if not type(item[1]) == type(str):
                    self.Append((item[0], str(item[1])))
                else:
                    self.Append(item)

            # Resize columns to fit largest string in each column
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        else:
            self.DeleteAllItems()
