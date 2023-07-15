import telebot
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = "YEAR TOKEN"

bot = telebot.TeleBot(TOKEN)

scheduler = BackgroundScheduler()
scheduler.start()
