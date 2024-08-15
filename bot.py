import telebot
import os
from pytube import YouTube

# Initialize the bot with your Telegram token from environment variable
token = os.environ.get('TELEGRAM_TOKEN')
if not token:
    raise ValueError("No TELEGRAM_TOKEN provided in environment variables.")

bot = telebot.TeleBot(token)

def markup_(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    res144 = telebot.types.InlineKeyboardButton("144p", callback_data="vid144")
    res360 = telebot.types.InlineKeyboardButton("360p", callback_data="vid360")
    res480 = telebot.types.InlineKeyboardButton("480p", callback_data="vid480")
    res720 = telebot.types.InlineKeyboardButton("720p", callback_data="vid720")
    res1080 = telebot.types.InlineKeyboardButton("1080p", callback_data="vid1080")
    markup.add(res144, res360, res480, res720, res1080)
    bot.send_message(message.chat.id, "Please select the resolution:", reply_markup=markup)
    return markup

@bot.message_handler(commands=['youtube'])
def you(message):
    bot.send_message(message.chat.id, 'Please paste the YouTube video URL:')
    bot.register_next_step_handler(message, process_url)

def process_url(message):
    global url
    url = message.text
    markup_(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.message:
        resolution_map = {
            "vid144": '144p',
            "vid360": '360p',
            "vid480": '480p',
            "vid720": '720p',
            "vid1080": '1080p'
        }
        resolution = resolution_map.get(call.data)
        if resolution:
            download_vid(call.message, resolution)

def download_vid(message, resolution):
    try:
        yt = YouTube(url)
        video_title = yt.title
        bot.send_message(message.chat.id, f"Downloading {video_title} in {resolution} resolution...")
        stream = yt.streams.filter(res=resolution).first()
        if stream:
            filename = stream.download()
            bot.send_message(message.chat.id, f"Downloading {video_title} in {resolution} resolution...")
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"Download completed: {video_title} in {resolution}")
            os.remove(filename)
        else:
            bot.send_message(message.chat.id, f"No video found in {resolution} resolution.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Start the bot
bot.polling()
