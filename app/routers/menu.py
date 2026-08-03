from fastapi import APIRouter, Depends, Query, status

from app.dependencies.menu import get_menu_service
from app.schemas.menu import (
    MenuCreateRequest,
    MenuResponse,
    MenuDetailResponse,
    PaginatedMenuResponse,
)
from app.services.menu import MenuService


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"],
)


@router.get(
    "",
    response_model=PaginatedMenuResponse,
)
def list_menus(
    page_number: int = Query(
        default=1,
        alias="pageNumber",
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        alias="pageSize",
        ge=1,
        le=100,
    ),
    service: MenuService = Depends(get_menu_service),
) -> PaginatedMenuResponse:
    """
    Retrieve a paginated list of menus.
    """

    return service.list(
        page_number=page_number,
        page_size=page_size,
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


@router.get(
    "/{menu_id}",
    response_model=MenuResponse,
)
def get_menu(
    menu_id: int,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """
    Retrieve a menu by its identifier.
    """

    return service.get(menu_id)


@router.delete(
    "/{menu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_menu(
    menu_id: int,
    service: MenuService = Depends(
        get_menu_service,
    ),
) -> None:
    """
    Logically delete a menu.
    """

    service.delete(menu_id)
