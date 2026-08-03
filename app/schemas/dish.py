from pydantic import BaseModel

from app.schemas.common import (
    ImageUrl,
    LocalizedDescription,
    LocalizedName,
    MealCode,
)


class DishCreateRequest(BaseModel):
    meal_code: MealCode

    name_es: LocalizedName
    name_en: LocalizedName

    description_es: LocalizedDescription
    description_en: LocalizedDescription

    image_url: ImageUrl

    availability: bool
    

class DishResponse(BaseModel):
    id: int

    meal_code: MealCode

    name_es: LocalizedName
    name_en: LocalizedName

    description_es: LocalizedDescription
    description_en: LocalizedDescription

    image_url: ImageUrl

    availability: bool