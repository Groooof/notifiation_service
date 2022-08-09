from fastapi import FastAPI
from v1.routers import router
from core.storage.database import database
from core.schemas import Settings


def get_app() -> FastAPI:
    app = FastAPI()
    app.title = 'Сервис уведомлений o-o'
    app.description = '''
    Данный сервис создан в рамках выполнения тестового задания на позицию backend-разработчика. 
    Реализует функционал рассылки сообщений клиентам по заданным параметрам, управления рассылками и сбора статистики.
    '''
    app.include_router(router)
    return app


app = get_app()


@app.on_event('startup')
async def startup():
    cfg = Settings()
    await database.create_pool(host=cfg.POSTGRES_HOST,
                               user=cfg.POSTGRES_USER,
                               password=cfg.POSTGRES_PASSWORD,
                               database=cfg.POSTGRES_DB,
                               port=cfg.POSTGRES_PORT)


@app.on_event('shutdown')
async def shutdown():
    await database.close_pool()










