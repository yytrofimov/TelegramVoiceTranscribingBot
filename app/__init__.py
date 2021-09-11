import commands
import telebot
import speech_recognition as sr
from pathlib import Path
import subprocess
import pathlib
import shutil
from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:
    TOKEN = os.environ.get("TOKEN")
    LANGS = ['en-US', 'ru-RU', 'sv-FI']
    SAVE_DATA = False


bot = telebot.TeleBot(Config.TOKEN, parse_mode=None)
r = sr.Recognizer()
