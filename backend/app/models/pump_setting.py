from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class PumpSettingBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    lower_limit_moist: Optional[float]
    upper_limit_moist: Optional[float]

class PumpSettingCreate(PumpSettingBase):
    plant_id: int
    lower_limit_moist: Optional[float]
    upper_limit_moist: Optional[float]

class PumpSettingUpdate(PumpSettingBase):
    pass

class PumpSettingInDB(IDModelMixin, DateTimeModelMixin, PumpSettingBase):
    plant_id: int
    lower_limit_moist: Optional[float]
    upper_limit_moist: Optional[float]

class PumpSettingPublic(IDModelMixin, DateTimeModelMixin, PumpSettingBase):
    plant_id: int
    lower_limit_moist: Optional[float]
    upper_limit_moist: Optional[float]