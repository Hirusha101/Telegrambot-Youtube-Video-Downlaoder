import telebot
from pytube import YouTube
import os

# Initialize bot with your Telegram token
bot = telebot.TeleBot('TELEGRAM_TOKEN')

# Helper function to create resolution selection markup
def markup_(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    resolutions = ['144p', '360p', '480p', '720p', '1080p']
    buttons = [telebot.types.InlineKeyboardButton(text, callback_data=text) for text in resolutions]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Please select the resolution:", reply_markup=markup)

# Handle the /youtube command
@bot.message_handler(commands=['youtube'])
def you(message):
    bot.send_message(message.chat.id, 'Please paste the YouTube video URL:')
    bot.register_next_step_handler(message, process_url)

# Process the YouTube URL and prompt for resolution
def process_url(message):
    global url
    url = message.text
    markup_(message)

# Handle the resolution selection
@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    resolution = call.data
    if resolution in ['144p', '360p', '480p', '720p', '1080p']:
        download_vid(call.message, resolution)
    else:
        bot.send_message(call.message.chat.id, "Invalid resolution selected.")

# Download video in the selected resolution
def download_vid(message, resolution):
    try:
        yt = YouTube(url)
        video_title = yt.title
        bot.send_message(message.chat.id, f"Downloading {video_title} in {resolution} resolution...")
        
        stream = yt.streams.filter(res=resolution).first()
        if stream:
            filename = stream.download()
            bot.send_message(message.chat.id, "Download complete!")
            
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"Download completed: {video_title} in {resolution}")
            
            os.remove(filename)
        else:
            bot.send_message(message.chat.id, f"No video found in {resolution} resolution.")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Start polling
bot.polling()
