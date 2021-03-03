import abc
import requests
import logging

from bs4 import BeautifulSoup

from Model.Anime import Anime
from Model.Episode import Episode

from WebDriver.Selenium import Selenium as browser

logging.basicConfig(
                    filename='app.log',
                    filemode='w',
                    format='%(asctime)s [%(filename)s: - %(funcName)5s()] | %(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%m/%d/%Y %H:%M:%S'
                    )
logger = logging.getLogger(__name__)


class Scraper(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getAnime') and
                callable(subclass.load_data_source) or
                NotImplemented)

    def __init__(self, baseUrl, webSiteName):
        self.baseUrl = baseUrl
        self.webSiteName = webSiteName
        self.requests = requests
        self.BeautifulSoup = BeautifulSoup
        self.Anime = Anime
        self.Episode = Episode
        self.browser = browser
        self.logger = logger
        pass

    # Return type is a List of Anime
    def getAnime(self, language, seriesName, nameFilter=None):
        raise NotImplementedError

    # Return type is a Episode
    def getEpisodes(self, url):
        raise NotImplementedError
