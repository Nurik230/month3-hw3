from config import bot
from aiogram import types, Dispatcher
from const import START_MENU_TEXT
from database import sql_commands


async def start_button(message: types.Message):
    sql_commands.Database().sql_insert_user_cmd(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name)

    print(message)
    with open(r"C:\Users\gulna\PycharmProjects\kurs-3\media\12334.gif", "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=START_MENU_TEXT.format(
                user=message.from_user.username
            ),
            parse_mode=types.ParseMode.MARKDOWN
        )


# async def quiz1(message: types.Message):
#     question = "Who invented Pyton"
#     option = [
#         "Volndevort",
#         "Harry Poter",
#         "Linus Torvalds",
#         "Guido Van Rossum",
#         "Witch"
#     ]
#     await bot.send_poll(
#         chat_id=message.from_user.id,
#         guestion=guestion,
#         option=option,
#         is_anonymous=False,
#         type='quiz',
#         correct_option_id=3
#     )

def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
