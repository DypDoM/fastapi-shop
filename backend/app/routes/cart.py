#Сделан 14
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict
from ..database import get_db
from ..services.cart_service import CartService
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/cart",
    tags=["cart"]
)

#Все это не сами роуты
class AddToCartRequest(BaseModel): #Происходит добавление в корзину
    product_id: int 
    quantity: int
    cart: Dict[int, int] = {} #Создаем массив корзины с данными указаными выше

class UpdateCartRequest(BaseModel): #Обновление корзины 
    product_id: int
    quantity: int
    cart: Dict[int, int] = {} #Создаем массив корзины с данными указаными выше

class RemoveFromCartRequest(BaseModel): #Удаление из корзины
    cart: Dict[int, int] = {} #Создаем массив корзины с данными кол-ва и айди продуктов

#Сами роуты
@router.post("/add", status_code=status.HTTP_200_OK)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db)): #Рекуест - запрос на добавление в корзину. Затем указали бд
    service = CartService(db) #Инициализируем сервис
    item = CartItemCreate(product_id=request.product_id, quantity=request.quantity) #Берем схемку и засовываем туда продукт айди и кол-во товара которое нужно добавить
    updated_cart = service.add_to_cart(request.cart, item) #Обновляем содержимое. И добавляем с помощью эдд ту карт в нашу корзину айтем (см. выше)
    return {"cart": updated_cart} #В конце возвращаем корзину. Словарь карт и новую корзину с товаром что было обновлено

@router.post("", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(cart_data: Dict[int, int], db: Session = Depends(get_db)): #Роутер получения всей информации о корзине
    service = CartService(db) #Указали сервис
    return service.get_cart_details(cart_data) #Функция выведет все данные, все продукты, которые в корзине у нас в данный момент находятся

@router.put("/update", status_code=status.HTTP_200_OK)
def update_cart_item(request: UpdateCartRequest, db: Session = Depends(get_db)): #Обновление корзины
    service = CartService(db) #Указали сервис
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity) #Берем схемку и засовываем туда продукт айди и кол-во товара которое нужно обновить
    updated_cart = service.update_cart_item(request.cart, item) #Обновляем содержимое. И добавляем с помощью эдд ту карт в нашу корзину айтем (см. выше)
    return {"cart": updated_cart} #В конце возвращаем корзину. Словарь карт и новую корзину с товаром что было обновлено

@router.delete("/remove/{product_id}", status_code=status.HTTP_200_OK)
def remove_from_cart(product_id: int, request: RemoveFromCartRequest, db: Session = Depends(get_db)): #Удаление корзины
    service = CartService(db) #Указали сервис 
    updated_cart = service.remove_from_cart(request.cart, product_id) #Вызываем функцию ремув карт. Помещаем туда корзину и айди товара который нужно удалить
    return {"cart": updated_cart} #В конце возвращаем корзину. Словарь карт и новую корзину с товаром что было обновлено