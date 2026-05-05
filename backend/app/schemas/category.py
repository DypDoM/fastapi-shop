#Создан четвертым. Здесь мы будем принимать и описывать параметры валидации например для полей которые необходимы для создания категорий
from pydantic import BaseModel, Field 


class CategoryBase(BaseModel): #Наследуем BaseModel который только что импортировали. На основе его мы будем настраивать и другие наши схемы
    #Общие поля для остальных схем 
    name: str = Field(..., min_length=5, max_length=100, 
        description="Category name") 
    slug: str = Field(..., min_length=5, max_length=100,
        description="URL-friendly category name")

class CategoryCreate(CategoryBase): #Схема для CategoryCreate(создания категории). Здесь мы просто наследуем параметры
    pass #Если пользов. вводит две выше перечисленные категории для создания то мы позволяем ему создать и пишем pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description='Unique category identifier') #Помимо наследуемых параметров мы еще будем выдавать и id

    class Config:
        from_attributes = True #Позволяет создавать схему напрямую из модели 