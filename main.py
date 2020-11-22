import fastapi

from application.api import downloader


api = fastapi.FastAPI()
api.include_router(downloader.downloading,
                   tags=['downloading'])