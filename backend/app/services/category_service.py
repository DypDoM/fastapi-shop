#Сделан 9
from sqlalchemy.orm import Session
from typing import List
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryResponse, CategoryCreate
from fastapi import HTTPException, status

class CategoryService: 
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db) #В остальных файлах прописывался функционал. Здесь просто указывается что такой то репозиторий будет работать с бд

    def get_all_categories(self) -> List[CategoryResponse]: #Хотим получить все категории. На выходе получаем список который выведется через схему
        categories = self.repository.get_all() #Получаем категории которые достаем с помощью репозитория (строка 10-11 в категори_репозиториес)
        return [CategoryResponse.model_validate(cat) for cat in categories] #Возвращаем с помощью схемы которая валидирует и показывает как правильно вообще возвращать данные. (cat - сокращенное категория)

    def get_category_by_id(self, category_id: int) -> CategoryResponse: #Категори возвращаем через категори респонс, чтобы он проверил на корректность и вывел в нужном формате
        category = self.repository.get_by_id(category_id) #Обращение к бд для нахождения нужного айди
        if not category: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category with id {category_id} not found'
            ) #Выводится ошибка если не нашел. Сообщение "По такому айди ничего не нашли"
        return CategoryResponse.model_validate(category) #Возвращем категорию через схемку

    def create_category(self, category_data: CategoryCreate) -> CategoryResponse: #category_data-массив с нашими данными на основе которых нужно создать категорию (с помощью класса Категори криейт)
        category = self.repository.create(category_data) #Создание категории
        return CategoryResponse.model_validate(category) #Создал категорию