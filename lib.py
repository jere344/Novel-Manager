# Every files that are often used in the other scripts


import configparser
import pathlib

# App will be the main app. Will be set by the main app when being started
app = None

__location__ = pathlib.Path(__file__).parent.resolve()

config = configparser.ConfigParser()
config.read(__location__.joinpath("config", "config.ini"), encoding="utf-8")

style = configparser.ConfigParser()
style.read(__location__.joinpath("config", "style.ini"), encoding="utf-8")

chapterlist = configparser.ConfigParser()
chapterlist.read(__location__.joinpath("config", "chapterlist.ini"), encoding="utf-8")

proxies = {"http": "http://193.31.27.123:80"}
