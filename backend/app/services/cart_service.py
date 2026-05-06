#Сделан 11
from sqlalchemy.orm import Session
from typing import Dict
from ..repositories.product_repository import ProductRepository
from ..schemas.cart import CartResponse, CartItem, \
                            CartItemCreate, CartItemUpdate #Обратный слеш это перенос строки
from fastapi import HTTPException, status


class CartService:
    def __init__(self, db: Session): #Базовая инициализация 
        self.product_repository = ProductRepository(db) 

    def add_to_cart(self, cart_data: Dict[int, int], item: CartItemCreate) -> Dict[int, int]: #cart_data - обязательно словарь где : айди продукта, кол-во. Получаем словарь который говорит о айдишинке товара и кол-ве
        product = self.product_repository.get_by_id(item.product_id) #Проверяем существует ли такой товар обращаясь к базе данных
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {item.product_id} not found'
            ) #Если нет то ошибка

        if item.product_id in cart_data: #Если айди товара есть в корзине. Так это сессия а каждая сессия это файлы куки которые пользователь прикладывает вот для этого такая проверка и нужна
            cart_data[item.product_id] += item.quantity #Увеличим кол-во товара
        else:
            cart_data[item.product_id] = item.quantity #Если в корзине еще нет такого товара то мы его просто добавляем

        return cart_data #Возвращаем корзину


    def update_cart_item(self, cart_data: Dict[int, int], item: CartItemUpdate) -> Dict[int, int]: #Изменение кол-ва товара. Схема такая же как и выше на строке 14. Толкьо используется другая схема
        #Если у нас такой товар уже в корзине
        if item.product_id not in cart_data:  #Если нет 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found in cart"
            ) #Выводим ошибку

        cart_data[item.product_id] = item.quantity #Меняем кол-во на новое которое указал пользователь
        return cart_data #Обновляем кол-во

    def remove_from_cart(self, cart_data: Dict[int, int], product_id: int) -> Dict[int, int]: #Удаление товара из корзины. тоже что и в 14.
        if product_id not in cart_data: #Если такого товара нет в корзине
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found in cart"
            )#Выдаем ошибку

        del cart_data[product_id] #Если есть удаляем товар
        return cart_data #Обновляем корзину

    def get_cart_details(self, cart_data: Dict[int, int]) -> CartResponse: 
        if not cart_data: #Проверка на существование корзины
            return CartResponse(items=[], total=0.0, items_count=0) #Инициализируем корзину заново и ставим нулевые параметры делая ее пустой

        product_ids = list(cart_data.keys()) #Собираем айди всех продуктов в список обращаясь к бд
        products = self.product_repository.get_multiple_by_ids(product_ids) #Достаем все продукты ориентируясь на айди с помощью базы данных
        products_dict = {product.id: product for product in products} #Собираем все наши продукты в словарь по найденным айди

        #Собираем вообще все значения нашей общей корзины. Базово ставим все на ноль
        cart_items = []
        total_price = 0.0
        total_items = 0

        for product_id, quantity in cart_data.items(): #Собираем продукты по айди, кол-ву из содержимого бд по продуктам
            if product_id in products_dict: #Если продукт айди находится в нашем словаре который мы инициализир. в нашем массиве данных то выполняются действия ниже
                product = products_dict[product_id] #Инициализируем продукт из нашего массива данных
                subtotal = product.price * quantity #Итоговая стоимость найденного продукта

                cart_item = CartItem(product_id=product.id, name=product.name,  
                    price=product.price, quantity=quantity, subtotal=subtotal,
                    image_url=product.image_url) #Карточка товара. Формируем с помощью схемку с помощью айди, имени, стоимости, кол-ва, итоговой стоимости, изображения

                cart_items.append(cart_item) #Добаляем все наши продукты поочередно
                total_price += subtotal #Итоговая стоимость корзины
                total_items += quantity #Итоговое кол-во товаров в корзине

        return CartResponse(items=cart_items, total=round(total_price), 
            items_count=total_items) #Возвращаем итоговое состояние корзины. Весь словарь с товарами который будет выведен карточками, итоговую стоимость и кол-во