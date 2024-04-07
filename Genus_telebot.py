import telebot
from telebot import types
import pymorphy2

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

morph = pymorphy2.MorphAnalyzer()

def replace_endings(text, target_gender):
    words = text.split()
    modified_words = []

    for word in words:
        parsed_word = morph.parse(word)[0]
        base_form_gender = parsed_word.tag.gender

        if base_form_gender == 'femn' and target_gender == 'masc':
            inflected_word = parsed_word.inflect({'masc'})
        elif base_form_gender != 'femn' and target_gender == 'femn':
            inflected_word = parsed_word.inflect({'femn'})
        else:
            inflected_word = None
                
        if inflected_word:
            modified_words.append(inflected_word.word)
        else:
            modified_words.append(word)

    modified_text = ' '.join(modified_words)
    return modified_text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я могу изменить род слов в предложении. Пожалуйста, отправьте мне предложение.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    msg_text = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

    bot.send_message(chat_id, "На какой род вы хотите изменить предложение?", reply_markup=markup)

    bot.register_next_step_handler(message, lambda m: handle_gender_choice(m, msg_text))

def handle_gender_choice(message, original_text):
    chat_id = message.chat.id
    gender = message.text.lower()

    if gender == 'мужской':
        target_gender = 'masc'
    elif gender == 'женский':
        target_gender = 'femn'
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите 'Мужской' или 'Женский'.")
        return

    modified_text = replace_endings(original_text, target_gender)
    bot.send_message(chat_id, f"{modified_text}")

bot.polling()