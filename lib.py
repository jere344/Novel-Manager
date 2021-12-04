# Every files that are often used in the other scripts


import configparser
import pathlib

__location__ = pathlib.Path(__file__).parent.resolve()

config = configparser.ConfigParser()
config.read(__location__.joinpath("config", "config.ini"), encoding="utf-8")

style = configparser.ConfigParser()
style.read(__location__.joinpath("config", "style.ini"), encoding="utf-8")

chapterlist = configparser.ConfigParser()
chapterlist.read(__location__.joinpath("config", "chapterlist.ini"), encoding="utf-8")

proxies = {"http": "http://193.31.27.123:80"}


class Standalone:
    """A class with the necessary method to replace a gui. Allow use of the app in command line ony"""

    def __init__(self) -> None:
        self.novel_selected = config.sections()[0] if config.sections() else None
        self.flask_running = False

    def SetLast(self, value):
        print(value)

    def UpdateMiddlePannel():
        pass

    def UpdateCover():
        pass


# App will be the main app. Will be set by the main app when being started
# Standalone is a replacement for test purpose and for use without gui but will be replaced when the gui is run

app = Standalone()
