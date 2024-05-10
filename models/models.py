from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_text = Column(String)  # Изменено на task_text для соответствия столбцу в БД
    # user_id = Column(Integer)   # Добавлены столбцы user_id и created_at
    # created_at = Column(String)
