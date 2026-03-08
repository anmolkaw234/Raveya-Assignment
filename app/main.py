from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.session import Base, engine

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(router)
