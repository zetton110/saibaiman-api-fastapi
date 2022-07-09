from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class PumpLogBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]

class PumpLogCreate(PumpLogBase):
    plant_id: int

class PumpLogUpdate(PumpLogBase):
    pass

class PumpLogInDB(IDModelMixin, DateTimeModelMixin, PumpLogBase):
    plant_id: int

class PumpLogPublic(DateTimeModelMixin, PumpLogBase):
    plant_id: int