from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(  #Отвечает за соединение с базой данных
    settings.database_url, # В config.py находится settings которая была инициализ. т.е Class settings
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Настройка соединения. Создается каждый раз когда фронт присылает запрос от пользователя(ищет категорию). Создает сессию на соединение с базой данных. После того как выводится что нужно сессия закрывается
Base = declarative_base() #Базовый класс для моделей в проекте

#Для штамповки сессии sessionmaker нужно две функции
def get_db(): #Суть в том чтобы вызвать новую сессию каждый раз когда нужна база данных передать данные от базы данных к сервису кот. хочет воспользов. данными и в конце закрыть 
    db = SessionLocal()
    try:
        yield db #Открывается для обработки запроса
    finally:
        db.close() #После обработки закрывается

def init_db():
    Base.metadata.create_all(bind=engine) #Инициализ бд с помощью engine заданного выше