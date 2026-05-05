#Сделан седьмым
from sqlalchemy.orm import Session
from typing import List, Optional
#Далее достаются модели
from ..models.category import Category
#Далее достаются схемы
from ..schemas.category import CategoryCreate

class CategoryRepository: #Провели инициализ. обозначили базу данных с которой нужно работать 
    def __init__(self, db: Session): #db: Session - база данных которая использует сессию
        self.db = db

    def get_all(self) -> List[Category]: #Метод для получения всех категорий которые у нас есть в базе данных 
        return self.db.query(Category).all() #Обращаемся к базе данных за всеми объектами в строке Категории

    def get_by_id(self, category_id: int) -> Optional[Category]: #Обращаемся к базе данных основываясь на id за определенной категорией. Optional - может вернуться а может и нет
        return self.db.query(Category).filter(Category.id == category_id).first() #Отправляемся в категории и фильтруем все по категори айди ориентируясь на переданный в запросе айди. Поэтому ==

    def get_by_slug(self, slug: str) -> Optional[Category]: 
        return self.db.query(Category).filter(Category.slug == slug).first()

    def create(self, category_data: CategoryCreate) -> Category: #Метод на создание категории в базе данных. Используется схема создания категории из схем
        db_category = Category(**category_data.model_dump()) #Берем данные которые нам дали в той схеме
        self.db.add(db_category) #Добавляем в базу данных
        self.db.commit() #Фиксируем
        self.db.refresh(db_category) #Обновляем инфу
        return db_category