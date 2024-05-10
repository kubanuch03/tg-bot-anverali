from decouple import config
import telebot

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.models import Task



bot = telebot.TeleBot(config("BOT_TOKEN"))
DB_URL = f'postgresql://{config("POSTGRES_USER")}:{config("POSTGRES_PASSWORD")}@{config("POSTGRES_HOST")}:{config("POSTGRES_PORT")}/{config("POSTGRES_DB")}'


Base = declarative_base()
engine = create_engine(DB_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




TOKEN = config("BOT_TOKEN")

#=====  start  ================================================================================

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, f"Привет, {user_name}! Я бот для Telegram, это тестовое задание для компании Anverali!")


#=====  To Do  ================================================================================

@bot.message_handler(commands=['add'])
def handle_add(message):
    task_description = message.text.replace('/add', '').strip()
    if task_description:
        try:
            new_task = Task(task_text=task_description)
            session.add(new_task)
            session.commit()
            bot.reply_to(message, "Задача успешно добавлена!")
        except Exception as e:
            print("Error adding task to database")
            print(e)
            bot.reply_to(message, "Произошла ошибка при добавлении задачи в базу данных.")
    else:
        bot.reply_to(message, "Пожалуйста, укажите описание задачи после команды /add.")


@bot.message_handler(commands=['tasks'])
def handle_tasks(message):
    try:
        tasks = session.query(Task).all()
        if tasks:
            task_list = "\n".join([f"{task.id}. {task.task_text}" for task in tasks])
            response = f"Список задач:\n{task_list}"
        else:
            response = "Список задач пуст."
    except Exception as e:
        print("Error retrieving tasks from database")
        print(e)
        response = "Произошла ошибка при получении списка задач из базы данных."
    
    bot.reply_to(message, response)




bot.polling()
