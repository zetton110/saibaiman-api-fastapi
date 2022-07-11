from enum import Enum
from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class ServiceType(str, Enum):
    typetalk = "TYPETALK"
    twitter = "TWITTER"

class NotificationSettingBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    service_type: Optional[ServiceType]
    api_url: Optional[str] = ""
    access_token: Optional[str] = ""
    access_secret: Optional[str] = ""
    consumer_key: Optional[str] = ""
    consumer_secret: Optional[str] = ""
    enabled: Optional[bool] = False

class NotificationSettingCreate(NotificationSettingBase):
    plant_id: int
    api_url: str = ""
    access_token: str = ""
    access_secret: str = ""
    consumer_key: str = ""
    consumer_secret: str = ""
    enabled: bool = False

class NotificationSettingUpdate(NotificationSettingBase):
    pass

class NotificationSettingInDB(IDModelMixin, DateTimeModelMixin, NotificationSettingBase):
    pass

class NotificationSettingPublic(IDModelMixin, DateTimeModelMixin, NotificationSettingBase):
    pass
