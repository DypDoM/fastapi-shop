#Сделан 16
#Этот файл примерно тоже самое что и manage.py на Джанго. Здесь указываются основные настройки и собираются все ранее написанныые части приложения воедино
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routes import products_router, categories_router, cart_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
) #Указываем основные настройки. В первую очередь название приложения из конфига. Урл документация - будем хранить на Апи и докс. redoc_url - это апи редок

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #Мидлвере прописывали в конфиге апп - он позволяет фронту правильно общаться с бэком. CORSMiddleware - встроенный Фастапи метод. Далее идут источники от которых мы можем принимать запросы. allow_credentials - может ли фронт отправлять на наш бэк куки и вообще с ним работать.
# allow_methods - могут быть и pad и patch, get, post и это строка разрешает их все. Ограничивают их когда используют микросервисы
# allow_headers - разрешают все заголовки

app.mount('/static', StaticFiles(directory=settings.static_dir), name='static') #StaticFiles - встроенная функция. static_dir - в конфиге

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(cart_router)

@app.on_event('startup') #Метод инициализации базы данных
def on_startup():
    init_db()

@app.get('/')
def root(): #По пути в декораторе существует функция которая там работает. Она возвращает сообщение и ссылочку на документацию
    return {
        'message': 'Welcome to fastapi shop API',
        "docs": "api/docs",
    }

@app.get('/health') #Метод который позволяет дать запрос на сервер с проверкой его работоспособности
def health_check():
    return {'status': 'healthy'}