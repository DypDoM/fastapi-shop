#Сделан 13
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.product_service import ProductService
from ..schemas.product import ProductResponse, ProductListResponse

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=ProductListResponse, status_code=status.HTTP_200_OK) #Репонс модел - через что выдаст ответ
def get_products(db: Session = Depends(get_db)): #По сути получаем лист всех продуктов с базы данных
    service = ProductService(db) #Передача списка всех продуктов из сервиса
    return service.get_all_products() #Вывод списка продуктов 

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK) #Нужен айди продукта для его вывода 
def get_product(product_id: int, db: Session = Depends(get_db)): #Получили бд открыли сессию
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router.get("/category/{category_id}", response_model=ProductListResponse, status_code=status.HTTP_200_OK) #/api/products/category/{category_id} -  во что превращает запрос. Используем ProductListResponse для возвращения массива данных с продуктами
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    service = ProductService(db) #Указали сервис
    return service.get_products_by_category(category_id) ##Возвращаем айди определенной категории для определнного товара