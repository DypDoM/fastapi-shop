#Сделан 17. Отвечает за запуск
import uvicorn
from app.config import settings #Импорт настроек проекта

if __name__ == "__main__":
    uvicorn.run(
        'app.main:app',
        host='127.0.0.1',
        port=8000,
        reload=settings.debug,
        log_level='info',
    ) #app.main:app - наше приложение. host - где мы это будем запускать. 