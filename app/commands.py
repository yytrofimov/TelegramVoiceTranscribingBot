from speech_recognition import AudioFile, Recognizer
from __init__ import *


@bot.message_handler(content_types=['voice', 'audio'])
def convert_audio_to_text(message):
    user_id = message.from_user.id
    message_date = str(message.date)
    message_dir = 'app/temp/{}/{}'
    pathlib.Path(message_dir.format(user_id, '')).mkdir(
        parents=True, exist_ok=True)
    chat_id = message.chat.id
    bot.send_message(chat_id, "Processing...")
    downloaded_file = bot.download_file(
        bot.get_file(message.voice.file_id).file_path)
    with open(message_dir.format(user_id, message_date+'.ogg'), 'wb') as new_file:
        new_file.write(downloaded_file)
    cmd = 'ffmpeg -hide_banner -loglevel error -y -i {} {}'.format(message_dir.format(
        user_id, message_date+'.ogg'), message_dir.format(user_id, message_date+'.wav'))
    subprocess.call(cmd, shell=True)
    user_audio_file = sr.AudioFile(
        message_dir.format(user_id, message_date+'.wav'))
    with user_audio_file as source:
        user_audio = r.record(source)
    callback = ''
    for lang in Config.LANGS:
        text = r.recognize_google(user_audio, language=lang, show_all=True)
        if text:
            callback += lang + ': ' + text['alternative'][0]['transcript']+'\n'
        else:
            callback += lang + ': ' + '???'+'\n'
    if callback:
        bot.reply_to(message, callback)
    else:
        bot.reply_to(message, "Try again!")
    if not Config.SAVE_DATA:
        shutil.rmtree(message_dir.format(user_id, ''))