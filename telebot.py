import requests, asyncio

from bs4 import BeautifulSoup as bs

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import  KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


bot = Bot(token=("7120028831:AAF44Tpl2s_niHe940-SSA_HQ4a45QxDykA"), parse_mode=ParseMode.HTML)

dp = Dispatcher()

def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)


start_kb = get_keyboard(
    "Погода Івано-Франкавськ",
    sizes=(2,),
)


@dp.message(F.text == "Погода Івано-Франкавськ")
async def weather(message: types.Message):
    r = requests.get("https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D1%96%D0%B2%D0%B0%D0%BD%D0%BE-%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA")
    html = bs(r.content, 'html.parser')

    for x in html.select("#content"):
        t_max = x.select('.temperature .max')[0].text
        t_min = x.select('.temperature .min')[0].text
        text = x.select('.wDescription .description')[0].text

    await message.answer(f"<b>Погода в Івано-Франківську</b>\n{t_min} {t_max}\n{text}", parse_mode="html")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
