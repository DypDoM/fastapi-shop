#Модель для категории товара. Была написана первой для форжен кей связи с продуктами
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Category(Base): #Наследует класс base который был прописан в Class Base
    __tablename__ = "categories"

#index=True что прописан везде ускоряет поиск по полю
    id = Column(Integer, primary_key=True, index=True) #Айдишник товара
    name = Column(String, unique=True, nullable=False, index=True) #Название товара. unique - не может быть товаров с одинков. назв.
    slug = Column(String, unique=True, nullable=False, index=True) # это уникальная строка для идентификации категории в URL-адресах.(Дипсик)

    products = relationship("Product", back_populates="category") #relationship - связь категории с товаром. Если нужно будет показать определенную категорию то sqlalchemy подтянет с бд нужную инфу

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>" #Возвращает строку где показывает id и название категории. Сделано для более удобного взаимодейств.