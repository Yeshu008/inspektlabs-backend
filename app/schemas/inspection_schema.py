from pydantic import BaseModel, HttpUrl, field_validator
from typing import Literal

class InspectionCreateSchema(BaseModel):
    vehicle_number: str
    damage_report: str
    image_url: HttpUrl

    @field_validator('image_url')
    @classmethod
    def validate_image_extension(cls, v: HttpUrl) -> HttpUrl:
        allowed_extensions = ('.jpg', '.jpeg', '.png')
        if not str(v).lower().endswith(allowed_extensions):
            raise ValueError("Image URL must end with .jpg, .jpeg, or .png")
        return v


class InspectionStatusUpdateSchema(BaseModel):
    status: Literal['reviewed', 'completed']