import requests

from bs4 import BeautifulSoup
from Scrapers.Scraper import Scraper

# https://animeheaven.ru/search?q=sword+art+online
# https://animeheaven.ru/search?q=sword+Art+online
# https://animeheaven.ru/search?q=sword+art+online
# https://animeheaven.ru/anime-list?order_by=latest&genre=all&type=all&released=all&audio=dub


class AnimeheavenScraper(Scraper):

    def __init__(self):
        super().__init__(baseUrl='https://animeheaven.ru', webSiteName='animeheaven')
    pass

    def addAnime(self, title, language, nameFilter):
        if (nameFilter != None and bool(nameFilter and nameFilter.strip())):
            return self.subOrDub(title, language) and nameFilter in title
        return self.subOrDub(title, language)

    def subOrDub(self, title, language):
        if (language != 'SUB'):
            return language.lower() in title.lower()
        return not ('DUB'.lower() in title.lower())

    def isRecent(self, container, className):
        classContainer = container.find('div', class_=f'{className}r')
        if (container.find('div', class_=className) != None):
            classContainer = container.find('div', class_=className)

        return classContainer.find(
            'div', class_='centerv').text.strip()

    def getAnime(self, language, seriesName, nameFilter=None):
        animeList = []

        requestsParams = {
            'q': seriesName
        }

        page = self.requests.get(
            self.baseUrl + '/search', params=requestsParams)

        soup = self.BeautifulSoup(page.content, 'html.parser')

        results = soup.find(class_='iepbox')

        animeContainers = results.find_all('div', class_='iepcon')

        for anime in animeContainers:

            titleContainer = anime.find('a', class_='cona')

            episodeCount = self.isRecent(anime, 'iepst2')
            
            airDate = self.isRecent(anime, 'iepst3')

            urlToAnime = titleContainer.get('href').replace(
                self.baseUrl + '/detail/', '')
            title = titleContainer.text.strip()

            if self.addAnime(title, language, nameFilter):
                anime = self.Anime(title=title,
                                   episodeCount=episodeCount,
                                   webSiteName=self.webSiteName,
                                   urlToAnime=urlToAnime,
                                   airDate=airDate
                                   )
                animeList.append(anime)

        return animeList

    def getEpisodes(self, url):
        raise NotImplementedError
