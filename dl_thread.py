import wx
import threading
import dlsv

RESET = False


class DownloadThread(threading.Thread):
    def __init__(self, search_list):
        threading.Thread.__init__(self)
        self._dl_list = search_list
        self.KILL = False

    def run(self):
        """Overrides Thread.run, and is called on Thread.start()

        Downloads each picture individually after checking kill flag

        Kill flag set True will stop process (should be set after new search)
        """
        for anime in self._dl_list:
            if not self.KILL:
                try:
                    dlsv.dl_image(anime)
                except Exception as e:
                    print(f"Something failed during download: \n{e}\n")
            else:
                print("Thread switch")
                break

        self.KILL = RESET

