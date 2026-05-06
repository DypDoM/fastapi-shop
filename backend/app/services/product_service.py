#Сделан 10
from sqlalchemy.orm import Session
from typing import List
from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate
from fastapi import HTTPException, status

class ProductService:
    def __init__(self, db: Session): #Инициализация бд продуктов и категорий
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    #Метод который должен вернуть все продукты которые есть на сайте
    def get_all_products(self) -> ProductListResponse: #Мы должны получить массив данных
        products = self.product_repository.get_all() #Репозиторий выводит все продукты
        products_response = [ProductResponse.model_validate(prod) for prod in products] #С помощью фор записываем и валидируем. Который возвращает только те поля которые нужно
        return ProductListResponse(products=products_response, total=len(products_response)) #Возвращаем продукты которые нужны и общее кол-во

    def get_product_by_id(self, product_id: int) -> ProductResponse: #На вход принимаем айди товара который нужно выдать и выдаем с помощью продакт респонс
        product = self.product_repository.get_by_id(product_id) #Берутся и ищутся все продукты по айди
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            ) #Выводит ошибка
        return ProductResponse.model_validate(product) #Найденное кол-во валидируется а затем выводится нужное

    def get_products_by_category(self, category_id: int) -> ProductListResponse: #На вход принимаем айди категории по которому фильтруем
        category = self.category_repository.get_by_id(category_id) #С помощью репозиторий для категорий вычисляем из бд с помощью айди нужную категорию
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            ) #Если не найдена то ошибка

        products = self.product_repository.get_by_category(category_id) #Далее по найденной выше категории находятся все продукты
        products_response = [ProductResponse.model_validate(prod) for prod in products] #Записываем результат в массив с помощью цикла фор и валидируем
        return ProductListResponse(products=products_response, total=len(products_response)) #Возвращаем с помощью Продактлистреспонсе все наши товары отфильтр.по категории и их кол-во

    def create_product(self, product_data: ProductCreate) -> ProductResponse: #Метод занимается созданием продукта 
        category = self.category_repository.get_by_id(product_data.category_id) #Обращается к категории по айди для нового товара
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product_data.category_id} does not exist"
            ) #Если нет то ошибка

        product = self.product_repository.create(product_data) #Если есть то создаем продукт который привязан к категории выше 
        return ProductResponse.model_validate(product) #Возвращаем новый продукт