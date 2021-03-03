import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters
)

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(asctime)s [%(filename)s: - %(funcName)5s()] | %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Stages
ONE, TWO, THREE, FOUR = range(4)


class TelegramBot:

    seriesName = None
    selectedSite = None

    def __init__(self, token, scrapers, language='SUB'):
        logging.info("Telegram Bot Started")
        self.updater = Updater(token, use_context=True)
        self.bot = self.updater.bot
        self.scrapers = scrapers
        self.language = 'SUB'
        self.main()
        pass

    def showScrapers(self, update: Update, context: CallbackContext) -> None:
        try:
            keyboard = []
            logging.info("Show Anime Sites")
            for scraper in self.scrapers:
                keyboard.append([InlineKeyboardButton(
                    scraper, callback_data=scraper)])

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text("Anime Sites", reply_markup=reply_markup)

            if context.args:
                self.seriesName = " ".join(context.args)
                return TWO

            return ONE
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ConversationHandler.END

    def askForAnimeName(self, update: Update, context: CallbackContext) -> None:
        try:
            query = update.callback_query

            query.answer()

            logging.debug("Anime To search for", query.answer())
            self.selectedSite = query.data

            query.edit_message_text(
                text="Enter Anime Name"
            )
            return TWO
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ConversationHandler.END

    def getAnime(self):
        try:
            keyboard = []

            animeList = self.scrapers[self.selectedSite].getAnime(
                language=self.language, seriesName=self.seriesName)

            if animeList:
                for anime in animeList:
                    print(
                        f"{anime.title}: {anime.episodeCount} [{anime.urlToAnime}]")
                    btnText = f"{anime.title}: {anime.episodeCount}"
                    keyboard.append([InlineKeyboardButton(
                        btnText, callback_data=anime.urlToAnime)])
                    pass

                return InlineKeyboardMarkup(keyboard)
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ConversationHandler.END

    def getAnimeMessageHandler(self, update: Update, context: CallbackContext) -> None:
        try:
            self.seriesName = update.message.text

            reply_markup = self.getAnime()

            if (reply_markup == None):
                update.message.reply_text(text="Anime not found")
                return ConversationHandler.END

            update.message.reply_text(
                self.selectedSite, reply_markup=reply_markup)

            return THREE
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ConversationHandler.END

    def getAnimeCallbackQueryHandler(self, update: Update, context: CallbackContext) -> None:
        try:
            query = update.callback_query
            query.answer()
            self.selectedSite = query.data

            reply_markup = self.getAnime()

            if (reply_markup == None):
                query.edit_message_text(text="Anime not found")
                return ConversationHandler.END

            query.edit_message_text(
                self.selectedSite, reply_markup=reply_markup)

            return THREE
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return ConversationHandler.END

    def getEpisodes(self, update: Update, context: CallbackContext) -> None:
        try:
            query = update.callback_query

            query.answer()

            query.edit_message_text(text=f"Searching...")

            self.bot.send_chat_action(
                chat_id=query.message.chat_id, action=ChatAction.TYPING)

            episodes = self.scrapers[self.selectedSite].getEpisodes(query.data)

            query.edit_message_text(text=str(episodes))

            return ConversationHandler.END
        except NotImplementedError:
            query.edit_message_text(
                text=f"Site: [{self.selectedSite}]\nget Episodes is not Implemented")
            return ConversationHandler.END
        except Exception as e:
            logger.error(e)
            query.edit_message_text(
                text=f"Site: [{self.selectedSite}]\nUnable to get Episodes")
            return ConversationHandler.END

    def main(self):
        try:
            dispatcher = self.updater.dispatcher

            conv_handler = ConversationHandler(
                entry_points=[CommandHandler('start', self.showScrapers)],
                states={
                    ONE: [
                        CallbackQueryHandler(self.askForAnimeName),
                    ],
                    TWO: [
                        MessageHandler(Filters.text & ~(
                            Filters.command), self.getAnimeMessageHandler),
                        CallbackQueryHandler(
                            self.getAnimeCallbackQueryHandler),
                    ],
                    THREE: [
                        CallbackQueryHandler(self.getEpisodes),
                    ]
                },
                fallbacks=[CommandHandler('start', self.showScrapers)]
            )

            dispatcher.add_handler(conv_handler)

            self.updater.start_polling()
            self.updater.idle()
        except Exception as e:
            self.logger.error(f"Error: {e}")
