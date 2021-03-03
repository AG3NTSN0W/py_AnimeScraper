import os
import sys
import logging

from Scrapers.NineAnimeScraper import NineAnimeScraper
from Scrapers.AnimeheavenScraper import AnimeheavenScraper
# from Scrapers.AnimelandScraper import AnimelandScraper

from Telegram.Telegram import TelegramBot as Telegram

logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(asctime)s | %(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%m/%d/%Y %H:%M:%S'
                    )
logger = logging.getLogger(__name__)


def main():

    scrapers = {
        NineAnimeScraper().webSiteName: NineAnimeScraper(),
        AnimeheavenScraper().webSiteName:  AnimeheavenScraper()
    }

    try:
        if (len(sys.argv) >= 2):
            token = sys.argv[1]
            language = sys.argv[2]
        else:
            token = os.environ['BOT_TOKEN']
            language = os.environ['LANGUAGE'].upper()

        Telegram(token=token, scrapers=scrapers, language=language)
    except Exception as e:
        logger.warning(f"{e} was not porvided")

    # anime = AnimeheavenScraper()
    # test = anime.getAnime(language='SUB', seriesName='attack on titan', nameFilter='')
    # for anime in test:
    #     print(f'Title: {anime.title},  \nAir Date:{anime.airDate}\n')

    pass

if __name__ == '__main__':
    main()
