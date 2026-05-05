#Создан пятым.
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .category import CategoryResponse


class ProductBase(BaseModel): #Также повторяется как и в моделях
    name: str = Field(..., min_length=5, max_length=200,
                            description="Product name") # ... - это обязательное поле
    description: Optional[str] = Field(None, description="Product description") #Optional - опциональное поле которое может не заполнятся. Поэтому Field(None
    price: float = Field(..., gt=0,
                            description="Product price(must be greater than 0")
    category_id: int = Field(..., description='Category ID')
    image_url: Optional[str] = Field(None, description='Product image URL')

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel): #То как мы будем видеть получаемую информацию из ip в определенном продукте 
    id: int = Field(..., description="Unique product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str] #Все медиафайлы и статик файлы не хранятся как файлы в видимой странице. Они хранятся в виде ссылок которые ведут к файлу
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category details") #Брали из импорта

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel): #Класс который будет выводить лист наших продуктов. Массив данных наших продуктов
    products: list[ProductResponse]
    total: int = Field(..., description='Total number of products')