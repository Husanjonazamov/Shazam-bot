import os.path
from aiogram import Bot,Dispatcher,executor
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from asos import Shazam
from db import DB

bot = Bot("6423614543:AAG4jxq5lIhGxvMGAKvKRDmfMg466nvtwvE")

dp = Dispatcher(bot)

admins = [
    5303925509
]
if not os.path.exists("users"):
    os.mkdir("users")
dp = Dispatcher(bot)

def is_admin(func):
    def decorator(msg):
        if msg.chat.id in admins:
            return func(msg)
        else:
            return

    return decorator
async def sendmessage(from_chat_id, message_id):
    users =DB.all()
    for user in users:
        await bot.copy_message(chat_id=user["user_id"],from_chat_id=from_chat_id,message_id=message_id)
        with open(f"users/{from_chat_id}.txt," "w") as file:
            file.write("")





admin_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
admin_keyboard.add(KeyboardButton(text="Statistika 🌡"))
admin_keyboard.add(KeyboardButton (text="Foydalanuvchilarga xabar yuborish "))
@dp.message_handler(text = "/admin")
@is_admin
async def admin_handler(msg: Message):
    await bot.send_message(msg.chat.id, "Admin panel", reply_markup=admin_keyboard)

@dp.message_handler(text = "Statistika 🌡")
@is_admin
async def handler(msg: Message):
    await bot.send_message(msg.chat.id, f"Bot Foydalanuvchilari {len(DB.all())} ta")


@dp.message_handler(commands=['start'])
async def start_handler(msg: Message):
    await msg.answer('''Salom! Qo‘shiqni topib berishim uchun, menga quyidagilardan birini yuboring:

• Qo‘shiq nomi yoki ijrochi ismi
• Qo'shiq matni
• Tik-Tokdan link
• Ovozli xabar
• Video xabar
• Audio
• Video
''')


@dp.message_handler(content_types=['text'])
async def text_handler(msg: Message):
    text = msg.text
    await bot.delete_message(msg.chat.id, msg.message_id)
    message_id = (await msg.answer("⏳")).message_id
    url = await Shazam.download(text)
    await bot.send_audio(msg.chat.id, audio=url, caption="Musiqa @musicstopmybot orqali yuklab olindi")
    await bot.delete_message(msg.chat.id,message_id)
@dp.inline_handler(lambda msg:True)
async def inline_handler(msg: InlineQuery):
    text = msg.query
    try:
        musics = await Shazam.search_async(text, 20)
    except Exception as e:
        print(e)
        return
    results = [
        InlineQueryResultArticle(description=music['subtitle'],
                                 id=str(index),
                                 title=music['title'],
                                 input_message_content=InputTextMessageContent(music['track_id']),
                                 thumb_url=music['image'])


        for
        index, music in enumerate(musics)
    ]
    await bot.answer_inline_query(inline_query_id=msg.id, results=results,cache_time=1)




executor.start_polling(dp)