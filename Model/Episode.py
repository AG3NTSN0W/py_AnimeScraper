class Episode:
    def __init__(self, title, webSiteName, lastEpisodeUrl, webSiteUrl, episodeCount="N/A"):
        self.title = title
        self.episodeCount = episodeCount
        self.webSiteName = webSiteName
        self.lastEpisodeUrl = lastEpisodeUrl
        self.webSiteUrl = webSiteUrl

    pass

    def __str__(self):
        return  f"Title: {self.title} \nEpisode Count: {self.episodeCount} \nUrl to Site {self.webSiteUrl} \nUrl To Episode {self.lastEpisodeUrl}"
pass