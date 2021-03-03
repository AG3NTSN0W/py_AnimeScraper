from Scrapers.Scraper import Scraper


class NineAnimeScraper(Scraper):

    def __init__(self):
        super().__init__(baseUrl='https://www13.9anime.to', webSiteName='9animes')
        pass

    def subOrDub(self, status):
        if status.find('div', class_='dub') != None:
            return 'DUB'

        return 'SUB'

    def showAnime(self, language, seriesLanguage, nameFilter, title):
        if (nameFilter != None):
            return seriesLanguage == language and nameFilter in title

        return seriesLanguage == language

    def getAnime(self, language, seriesName, nameFilter=None):
        try:
            animeList = []

            requestsParams = {
                'language': language,
                'sort': 'default',
                'keyword': seriesName
            }

            page = self.requests.get(
                self.baseUrl + '/filter', params=requestsParams)

            self.logger.info(
                f"Site Name: [{self.webSiteName}], Anime URL: [{page.url}]")

            soup = self.BeautifulSoup(page.content, 'html.parser')

            results = soup.find(class_='anime-list')

            animeContainers = results.find_all('li')

            if animeContainers != None:

                for anime in animeContainers:
                    titleContainer = anime.find('a', class_='name')
                    title = titleContainer.text.strip()

                    episodeCount = anime.find(
                        'div', class_='ep').text.strip()

                    seriesLanguage = self.subOrDub(anime)

                    if (None in (title, episodeCount)):
                        continue

                    urlToAnime = titleContainer.get('href').replace(
                        self.baseUrl + '/watch/', '')

                    if self.showAnime(language, seriesLanguage, nameFilter, title):
                        anime = self.Anime(title=title,
                                           episodeCount=episodeCount,
                                           webSiteName=self.webSiteName,
                                           urlToAnime=urlToAnime
                                           )

                        animeList.append(anime)
                    pass
                pass

                return animeList
        except Exception as e:
            self.logger.error(
                f"Site Name: [{self.webSiteName}], Anime URL: [{animeUrl}], Error: {e}")
            return []    
        pass

    def getEpisodes(self, url):

        try:
            animeUrl = self.baseUrl + url

            self.logger.info(
                f"Site Name: [{self.webSiteName}], Episode URL: [{animeUrl}]")

            page = self.browser().loadPage(animeUrl)

            soup = self.BeautifulSoup(page, 'html.parser')

            title = soup.title.string

            results = soup.find(id='servers-containerf')

            return self.Episode(title=title,
                                webSiteName=self.webSiteName,
                                lastEpisodeUrl=animeUrl,
                                webSiteUrl=self.baseUrl
                                )
        except Exception as e:
            self.logger.error(
                f"Site Name: [{self.webSiteName}], Episode URL: [{animeUrl}], Error: {e}")
            return None