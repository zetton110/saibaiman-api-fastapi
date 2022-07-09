from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class PumpSettingBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    need_pump: Optional[float]
    complete_pump: Optional[float]

class PumpSettingCreate(PumpSettingBase):
    plant_id: int
    need_pump: Optional[float]
    complete_pump: Optional[float]

class PumpSettingUpdate(PumpSettingBase):
    pass

class PumpSettingInDB(IDModelMixin, DateTimeModelMixin, PumpSettingBase):
    plant_id: int
    need_pump: Optional[float]
    complete_pump: Optional[float]

class PumpSettingPublic(DateTimeModelMixin, PumpSettingBase):
    plant_id: int
    need_pump: Optional[float]
    complete_pump: Optional[float]