from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.sql_commands import Database




class FormStates(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    married = State()
    photo = State()



async def fsm_start(message: types.Message):
    await message.reply("Отправить мне свой новый никнейм")
    await FormStates.nickname.set()

async def load_nickname(message:types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data["nickname"] = message.text

    await FormStates.next()
    await message.reply("Отправь мне свой возраст, используй только числа")

async def load_age(message:types.Message,
                        state: FSMContext):
    try:
        if type(int(message.text)) != int:

            await message.reply("Говорил же отправлять числа," 
                                "Пожалуйста запустите регистрацию заново")
            await state.finish()
        else:
            async with state.proxy() as data:
                data["age"] = message.text
                await FormStates.next()
                await message.reply("Отправь мне свою биографию или хобби")
    except ValueError as e:
        print(f"FSMage {e}")
        await message.reply(("Говорил же отправлять числа," 
                                "Пожалуйста запустите регистрацию заново"))



async def load_bio(message:types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data["bio"] = message.text

    await FormStates.next()
    await message.reply("Вы женаты\замужем ? (если не хотите отвечать , отправьте знак минус пожалуйста")

async def load_married(message:types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data["married"] = message.text

    await FormStates.next()
    await message.reply("Отправь мне свою фото(не в разрешений файла)")
async def load_photo(message: types.Message,
                     state: FSMContext):
    # phto = await message.photo[-1].get_file()
    path = await message.photo[-1].download(
        destination_dir=r"\Users\gulna\PycharmProjects\kurs-3\media"
        )
    async with state.proxy() as data:
        with open(path.name, 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"*Nickname:* {data['nickname']}\n"
                        f"*Age:* {data['age']}\n"
                        f"*Bio:* {data['bio']}\n"
                        f"*Married:* {data['married']}\n",
                parse_mode=types.ParseMode.MARKDOWN
            )
def register_fsm_form_handler(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['signup'])
    dp.register_message_handler(load_nickname,
                                state=FormStates.nickname,
                                content_types=['text'])
    dp.register_message_handler(load_age,
                                state=FormStates.age,
                                content_types=['text'])
    dp.register_message_handler(load_bio,
                                state=FormStates.bio,
                                content_types=['text'])
    dp.register_message_handler(load_married,
                                state=FormStates.married,
                                content_types=['text'])
    dp.register_message_handler(load_photo,
                                state=FormStates.photo,
                                content_types=ContentType.PHOTO)