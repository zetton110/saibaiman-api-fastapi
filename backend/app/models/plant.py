from enum import Enum
from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class PlantType(str, Enum):
    fruit = "FRUIT"
    vegetable = "VEGETABLE"
    other = "OTHER"

class PlantBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    name: Optional[str]
    fullname: Optional[str]
    plant_type: Optional[PlantType]
    description: Optional[str]

class PlantCreate(PlantBase):
    name: str
    plant_type: PlantType

class PlantUpdate(PlantBase):
    pass

class PlantInDB(IDModelMixin, DateTimeModelMixin, PlantBase):
    name: str
    plant_type: PlantType

class PlantPublic(IDModelMixin, DateTimeModelMixin, PlantBase):
    name: str
    fullname: str
    plant_type: PlantType
    description: str

class PlantPublicWithoutTS(IDModelMixin, PlantBase):
    name: str
    fullname: str
    plant_type: PlantType
    description: str