#Сделан 8
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.product import Product
from ..schemas.product import ProductCreate

class ProductRepository: #Инициализ
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]: #Получим все продукты
        return self.db.query(Product).options(joinedload(Product.category)).all() #Сначала загружаем все продукты а затем добавлям оптионс (опционально) выгружать категорию

    def get_by_id(self, product_id: int) -> Optional[Product]: #Получим все айди
        return (
            self.db.query(Product) #Берем все продукты из базы данных
            .options(joinedload(Product.category)) #Снова добавляем категории чтобы появилась детальная инф о них
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_category(self, category_id: int) -> List[Product]: #Получать товары сразу отфильтрованые по категории
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id)
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product: #Метод на создание продукта. Используется схема продакт
        db_product = Product(**product_data.model_dump()) #Сначала указали модель создания а затем указали продакт дата котурую дал пользов. который хочет создать продукт (заполнил это в схемах). model_dump просто загружаем
        self.db.add(db_product) #добавляем продукт в базу данных
        self.db.commit() #Фиксируем
        self.db.refresh(db_product) #Обновляем
        return db_product #Возвращаем

    def get_multiple_by_ids(self, product_ids: List[int]) -> List[Product]: #Пытаемся найти массив продуктов по айди
        return (
            self.db.query(Product) #Идем в базу данных
            .options(joinedload(Product.category)) #Делаем опцион. сортировку по категориям
            .filter(Product.id.in_(product_ids)) #Фильтруем что продакт айди который мы нашли должен соответ. хотя бы одному который у нас есть
            .all() #Вывести все
        )