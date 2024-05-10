from decouple import config
import telebot
from decouple import config
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание базового класса модели
Base = declarative_base()

# Определение модели задачи
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_text = Column(String)  # Изменено на task_text для соответствия столбцу в БД
    # user_id = Column(Integer)   # Добавлены столбцы user_id и created_at
    # created_at = Column(String)

# Получение параметров подключения к базе данных из переменных окружения
DB_URL = f'postgresql://{config("POSTGRES_USER")}:{config("POSTGRES_PASSWORD")}@{config("POSTGRES_HOST")}:{config("POSTGRES_PORT")}/{config("POSTGRES_DB")}'

# Создание соединения с базой данных
engine = create_engine(DB_URL)

# Создание таблицы, если она не существует
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создание объекта бота
TOKEN = config("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, f"Привет, {user_name}! Я бот для Telegram, подключенный к PostgreSQL с использованием SQLAlchemy.")

# Обработчик команды /add
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
# Запуск бота
bot.polling()
