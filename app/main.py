from fastapi import FastAPI

from app.routers.flight import router as flight_router
from app.routers.menu import router as menu_router
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title="Flight Menu Management API",
    description="REST API for managing flight menus.",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(
    flight_router,
)

app.include_router(
    menu_router,
)