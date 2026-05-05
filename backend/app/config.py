#Данный файл является трафаретным образом который передается из проект в проект. Может подвергаться минимальной редактуре.
from pydantic_settings import BaseSettings

class Settings(BaseSettings): #Задает настройки
    app_name: str = "FastAPI Shop" #Название приложения
    debug: bool = True #Так как данный проект в разработке дебаг нужен для отслеживания состояния проекта
    database_url: str = "sqlite:///./shop.db"
    cors_origins: list = [      #Пути от которых будет принимать наш бэкенд запросы. 5173 это фронтенд
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ] #Для того чтобы наш ip принимал запрос от фронта нужно указать это все здесь. Http локал хост так как будем локально запускать
    static_dir: str = "static"
    images_dir: str = "static/images"

    class Config:
        env_file = ".env"

settings = Settings()