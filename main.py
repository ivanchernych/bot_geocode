from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram.ext import Application, MessageHandler, filters
import datetime
from translate import Translator
from telegram import ReplyKeyboardMarkup
from getting_coordinates import getting
import aiohttp
import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def geocoder(update, context):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": update.message.text,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    print(response.url)

    tompony = getting(response)

    if tompony is False:
        await update.message.reply_text(
            f'по адресу - {update.message.text} ничего не найдено, вашего адреса не существует!',
        )
        return

    ad = "{0},{1}".format(tompony[0], tompony[1])

    delta = "0.009"

    map_params = {
        "ll": ad,
        "spn": ",".join([delta, delta]),
        "l": "map",
        "pt": f'{ad},pm2dgl,'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    await context.bot.send_photo(
        update.message.chat_id,
        response.url,
        caption=f"по адресу - {update.message.text} найдено:"
    )


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("geocoder", geocoder))
application.add_handler(CommandHandler("translate", get_response))
application.run_polling()
