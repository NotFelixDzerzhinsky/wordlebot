import logging
from aiogram import Bot, Dispatcher, executor, types
import bot_token
from work import get_word, get_verdict, check_user_message, transform_verdict, init
from stats import change_leaderboard, get_leaderboard, get_stats

TOKEN = bot_token.Token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
count_attempts = 6

class Task(object):
    def __init__(self, word, verdicts, attempts):
        self.word = word
        self.verdicts = verdicts
        self.attempts = attempts

current_task = dict()

@dp.message_handler(commands=['start', 'help'])
async def send_help(message : types.Message):
    await message.answer("Данный telegram бот позволяет играть неограниченное количество раз в день в известную игру wordle.\n"
    "На данный момент работает только версия на русском языке.\n"
    "Для того чтобы начать игру, пропишите /start_wordle и далее вам нужно будет угадать загаданное слово за 6 попыток. "
    "С правилами можно ознакомиться на сайте данной игры или написав /rules.\n"
    "Для того чтобы узнать свою статистику, пропишите /stats. А для того чтобы увидеть список лучших, пропишите /leaderboard.\n"
    "На данный момент можно вводить все возможные комбинации букв, поэтому просьба, используйте реальные слова и контролируйте себя сами\n"
    "Желаю приятной игры😊😊")

@dp.message_handler(commands=['rules'])
async def send_rules(message : types.Message):
    await message.answer("Скоро будет добавлено(наверное)")

@dp.message_handler(commands=['leaderboard'])
async def send_leaderboard(message : types.Message):
    await message.answer(get_leaderboard())

@dp.message_handler(commands=['stats'])
async def send_stats(message : types.Message):
    await message.answer(get_stats(message.from_user))

@dp.message_handler(commands=['start_wordle'])
async def send_task(message : types.Message):
    userid = message.from_user.id
    user_message = message.text
    if userid in current_task:
        if current_task[userid].word != "":
            await message.answer("Закончите предыдущий раунд")
            return
    current_task[userid] = Task(get_word(), [], count_attempts)

    await message.answer("Игра началась! На каждом ходе введите слово из 5 букв и вам будет выдан вердикт")

@dp.message_handler()
async def simple_message(message : types.Message):
    userid = message.from_user.id
    user_message = message.text

    if userid in current_task and current_task[userid].word != "":
        user_message = user_message.lower()
        if check_user_message(user_message) == True:
            result = get_verdict(current_task[userid].word, user_message)
            result = transform_verdict(result)

            current_task[userid].verdicts.append(result)
            current_task[userid].attempts -= 1

            if result == "🟩🟩🟩🟩🟩":
                result += "\nПоздравляю, ты угадал слово!"
                await message.answer(result)
                all_verdicts = ""
                all_verdicts += "Wordle " + str(len(current_task[userid].verdicts)) + "/6:\n"
                for s in current_task[userid].verdicts:
                    all_verdicts += s + "\n"
                await message.answer(all_verdicts)
                change_leaderboard(message.from_user, len(current_task[userid].verdicts))
                current_task[userid] = Task("", [], 0)
                return
            else:
                if current_task[userid].attempts >= 5:
                    result += "\nОсталось ещё " + str(current_task[userid].attempts) + " попыток"
                elif current_task[userid].attempts >= 2:
                    result += "\nОсталось ещё " + str(current_task[userid].attempts) + " попытки"
                elif current_task[userid].attempts == 1:
                    result += "\nОсталась ещё " + str(current_task[userid].attempts) + " попытка"
                else:
                    result += "\nТы не смог отдагать слово " + current_task[userid].word.upper() + " :с \n"
                    await message.answer(result)
                    all_verdicts = "Wordle " + str(len(current_task[userid].verdicts)) + "/6:\n"
                    for s in current_task[userid].verdicts:
                        all_verdicts += s + "\n"
                    await message.answer(all_verdicts)
                    change_leaderboard(message.from_user, 0)
                    current_task[userid] = Task("", [], 0)
                    return
                await message.answer(result)
        else:
            await message.answer("Неверно записано слово, попробуйте ещё раз")
    else:
        await message.answer("Я не знаю, что вам ответить :(")
        

if __name__ == '__main__':
    init()
    executor.start_polling(dp, skip_updates=True)

