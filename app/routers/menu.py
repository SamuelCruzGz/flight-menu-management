from fastapi import APIRouter, Depends

from app.dependencies.menu import get_menu_service
from app.schemas.menu import (
    MenuCreateRequest,
    MenuResponse,
)
from app.services.menu import MenuService


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"],
)


@router.post(
    "",
    response_model=MenuResponse,
    status_code=201,
)
def create_menu(
    request: MenuCreateRequest,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """
    Create a menu and its associated dishes.
    """

    return service.create(request)