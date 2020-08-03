import wx

# TODO: Add Licenses for Jikan and AnimuGLU
class LicensesPopup(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(LicensesPopup, self).__init__(parent, *args, **kwargs)

        panel = wx.Panel(self)

        self.btn = wx.Button(panel, wx.ID_OK, label="ok", size=(50, 20), pos=(0, 0))

