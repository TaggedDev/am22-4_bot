from constants import CANCEL_KEYBOARD, SUBJECTS_KEYBOARD, SUBJECTS_LIST
from subject import Subject

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

with open('token.txt', 'r') as file:
    token = file.readline()

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    user_subject = State()  # Will be represented in storage as 'Form:user_subject'
    number = State()  # Will be represented in storage as 'Form:number'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Welcome screen when player types /help or /start
    """
    await message.reply("Телеграм-бот для группы ПМ22-4. Выберите предмет", reply_markup=SUBJECTS_KEYBOARD)
    await Form.user_subject.set()
 

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Назад', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await send_welcome(message)


@dp.message_handler(lambda message: not (message.text in SUBJECTS_LIST.keys()), state=Form.user_subject)
async def process_subject_invalid(message: types.Message, state: FSMContext):
    """
    Process invalid user input (subject)
    """
    await message.reply("Используйте клавиатуру")


@dp.message_handler(lambda message: message.text in SUBJECTS_LIST, state=Form.user_subject)
async def process_subject(message: types.Message, state: FSMContext):
    """
    Process chosen subject
    """
    async with state.proxy() as data:
        data['user_subject'] = message.text
        Form.subject = SUBJECTS_LIST[message.text]
        

    await Form.next()
    await message.reply("Напишите номер, который нужно скинуть")


async def process_number_invalid(message: types.Message, subject: Subject) -> None:
    await message.reply(subject.invalid_number_message, reply=CANCEL_KEYBOARD)


@dp.message_handler(state=Form.number)
async def process_number(message: types.Message, state: FSMContext) -> None:
    """
    Process chosen number
    """ 
    file = await Form.subject.get_file(message.text)
    
    if file.is_file():
        with open(file, 'rb') as attachment:
            ext = file.name[-3:]
            if ext == 'png':
                await bot.send_photo(message.chat.id, photo=attachment)
            else:
                await bot.send_document(message.chat.id, document=attachment)
    else:
        await process_number_invalid(message, Form.subject)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)