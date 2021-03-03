import requests

from bs4 import BeautifulSoup
from Scrapers.Scraper import Scraper

# https://www.animeland.us/?s=black+clover


class AnimelandScraper(Scraper):

    def __init__(self):
        super().__init__(baseUrl='https://www.animeland.us/', webSiteName='justdubs')
    pass

    def showAnime(self, nameFilter, title):
        if (nameFilter != None):
            return nameFilter in title

        return True

    def getAnime(self, language, seriesName, nameFilter=None):

        params = {
            "s": seriesName
        }

        page = requests.get(url=self.baseUrl, params=params)

        soup = BeautifulSoup(page.content, 'html.parser')

        result = soup.find(class_='video_thumb_content')

        animeContainers = result.find_all('div', class_='new_added')

        if animeContainers != None:
            print(
                f"Series Name: {seriesName}, \nLanguage: {language}, \nFilter: {nameFilter} \nFrom: {self.webSiteName} \nurl: {self.baseUrl}")
            print()

            for elem in animeContainers:
                title = elem.find('div', class_='title')

                if None in title:
                    continue

                title = title.text.strip()

                if self.showAnime(nameFilter, title):
                    print(title + ':', ' N/A')
                    print()
        return
