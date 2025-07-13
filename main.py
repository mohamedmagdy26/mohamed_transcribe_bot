import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer " + OPENAI_API_KEY},
            files={"file": f},
            data={"model": "whisper-1"}
        )
    return response.json().get("text")

@bot.message_handler(content_types=['voice', 'audio', 'video'])
def handle_media(message):
    file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id if message.audio else message.video.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    with open("temp.ogg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        text = transcribe_audio("temp.ogg")
        bot.reply_to(message, text or "ماقدرتش أفرغ الصوت 😢")
    except Exception as e:
        bot.reply_to(message, f"حصل خطأ: {e}")

bot.polling()
