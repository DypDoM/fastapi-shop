#Модель для товара. Была написана второй 
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Product(Base):
    __tablename__ = "products" #__tablename__ - То как оно будет отображаться в базе данных

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text) #Описание товара
    price = Column(Float, nullable=False) #Стоимость с плавающей точкой
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False) #ForeignKey("categories.id") - делается связь с моделью category.py и привязывает продукт к опред. объекту категорию с помощью айдишника. Каждый товар должен быть привязан к категории
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products") #relationship - связь товара с категорией. Если нужно будет показать определенный товар то sqlalchemy подтянет с бд нужную инфу

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>" #Возвращает строку где показывает id и название продукта. Сделано для более удобного взаимодейств.