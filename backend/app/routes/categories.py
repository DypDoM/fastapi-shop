#Сделан 12
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.category_service import CategoryService
from ..schemas.category import CategoryResponse

router = APIRouter(
    prefix="/api/categories",
    tags=['categories'] #Нужен для того чтобы правильно структурировать финальный адрес в документации которую можно посмотреть после запуска
) #Инициализация роута. Префикс - ссылка; перед ней добавится домен автоматом; после нее ставятся методы для фильтрации

#Указали Категори Респонс, указали бд и сказали сервису гет олл категорис обратиться к бд для взятия всех категорий после чего в необходим формате выдай ответ в виде списка категорий
@router.get("", response_model=List[CategoryResponse], 
            status_code=status.HTTP_200_OK) #Первый путь с помощью декоратора регистрируем. Пустые кавычки - это /api/categories. 
        #Далее идет статус код -  это HTTP‑код ответа, который сервер возвращает клиенту (браузеру, другому сервису) вместе с данными. Он коротко сообщает результат обработки запроса
        #status.HTTP_200_OK (можно не указывать) — числовая константа (200) из модуля fastapi.status, которая означает «Запрос выполнен успешно, данные переданы».
def get_categories(db: Session = Depends(get_db)): #С помощью метода гет дб достаем базу данных из ..database
    service = CategoryService(db) #Делаем сессию
    return service.get_all_categories() #Возвращаем все категории

@router.get('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK) #Фильтрация по определенной категории. Категори айди принимается на вход чтобы отфильтровать по опред категории
def get_category(category_id: int, db: Session = Depends(get_db)): #Получили бд открыли сессию
    service = CategoryService(db) #Указываем сервис через который даст данные с указанием бд через которую это нужно сделать
    return service.get_category_by_id(category_id) #Возвращаем айди определенной категории 
#Человек через фронт осуществляет запрос. Категори айди принимает запрос и в первую очередь запрос идет на префикс
#Далее к префиксу добавляется категори айди (23 строка) и на выходе идет примерно след. ссылка - domen.com/api/categories/{category_id}.
#В /{category_id} подставляется тот айди который хотят посмотреть. @router.get как раз отвечает за принятие гет запроса и фильтрации валидации нужной категории
#Если пойдет что то не так то ошибка перехватится либо в схемах либо в сервисе