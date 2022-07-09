from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class MoistLogBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    moist: Optional[float]

class MoistLogCreate(MoistLogBase):
    plant_id: int
    moist: float

class MoistLogUpdate(MoistLogBase):
    pass

class MoistLogInDB(IDModelMixin, DateTimeModelMixin, MoistLogBase):
    plant_id: int
    moist: float

class MoistLogPublic(DateTimeModelMixin, MoistLogBase):
    plant_id: int
    moist: float