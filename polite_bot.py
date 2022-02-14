import telebot
from telebot.types import BotCommand, Message
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()
_p = morph.parse("сталь")[0]
print(_p.tag.case)
word = ""

messageCount = 0
maxMessageCount = 2

bot = telebot.TeleBot("5156546483:AAFD2sMMH4soESeuv0mZPIF4ZJfFlua8LQ0")
bot.set_my_commands(
    commands=
    [
        BotCommand("apologize", "Make Him apologize"),
        BotCommand("start", "Initialize the bot")

    ]
)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, "Приветствую, но я не в духе")

@bot.message_handler(commands=['apologize'])
def send_apologize(message: Message):
    bot.send_message(message.chat.id, getPhrase())


@bot.message_handler(func=lambda message: True)
def echo_all(message: Message):
    global messageCount
    global word
    global morph
    global maxMessageCount

    if message.text.lower() == "бот извинись" or message.text == "@VeryElegantBot извинись":
        bot.send_message(message.chat.id, getPhrase())
        return
    messageCount += 1
    if messageCount == maxMessageCount:
        sep = message.text.split(" ")
        for _word in sep:
            p = morph.parse(_word)[0]
            if p.tag.POS == "NOUN":

                newP = p.inflect({'ablt'})
                if p.tag.number == "plur":
                    newP = p.inflect({'plur', 'ablt'})
                word = newP.word
                bot.send_message(message.chat.id, "Подите прочь со " +
                                 getchangingWord(newP.tag.gender, newP.tag.number)
                                 + " " + word)
                messageCount = 0
                maxMessageCount = random.randint(15, 30)
                print(maxMessageCount)
                return
            else:
                messageCount = 0

        messageCount = 0



def getPhrase():
    num = random.random()
    if num <= 0.3:
        return "Простите, виноват"
    if 0.3 <= num < 0.6:
        return "Великодушно извините"
    if 0.6 <= num < 0.9:
        return "Не взыщите"
    if num >= 0.9:
        return "Ах, оставьте..."


def getchangingWord(gender, number):
    if gender == "femn" and number == "sing":
        return "cвоей"
    if gender == "masc" and number == "sing":
        return "cвоим"
    return "cвоими"


bot.infinity_polling()
