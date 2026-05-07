#Сделан 15
#Здесь нужно все зарегестрировать. Нужно использовать все импорты которые есть в routes и 
from .products import router as products_router
from .categories import router as categories_router
from .cart import router as cart_router

__all__ = ["products_router", "categories_router", "cart_router"]