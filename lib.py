# Every files that are often used in the other scripts


import configparser
import pathlib

__location__ = pathlib.Path(__file__).parent.resolve()
from kivy.utils import platform

user_os = platform

if platform == "win" or platform == "linux":
    DATA__location__ = __location__.joinpath("DATA")
    config__location__ = __location__.joinpath("config")
    book__location__ = __location__.joinpath("book")

elif platform == "android":
    pass

elif platform == "macosx":
    raise Exception(
        """Sorry ! mac os isn't supported yet.
    If you still want to try Novel Manager, build from source and modify user_os to 'win' or 'linux'
    """
    )

elif platform == "ios":
    raise Exception(
        """Sorry ! ios isn't supported yet.
    If you still want to try Novel Manager, build from source and modify user_os to 'android'
    """
    )
elif platform == "unknown":
    raise Exception(
        """Sorry ! Your os is not recognised.
    If you still want to try Novel Manager, build from source and modify user_os to a string of your os :
    ‘win’, ‘linux’, ‘android’, ‘macosx’ or ‘ios’
     """
    )


config = configparser.ConfigParser()
config.read(config__location__.joinpath("config.ini"), encoding="utf-8")

style = configparser.ConfigParser()
style.read(config__location__.joinpath("style.ini"), encoding="utf-8")

chapterlist = configparser.ConfigParser()
chapterlist.read(config__location__.joinpath("chapterlist.ini"), encoding="utf-8")

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

