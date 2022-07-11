from enum import Enum
from typing import Optional
from xmlrpc.client import Boolean, boolean
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class ServiceType(str, Enum):
    typetalk = "TYPETALK"
    twitter = "TWITTER"

class NotificationBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    service_type: Optional[ServiceType]
    notified_to_service: Optional[bool] = False
    message: Optional[str] = ""

class NotificationCreate(NotificationBase):
    plant_id: int
    service_type: ServiceType
    notified_to_service: bool = False
    message: str = ""

class NotificationUpdate(NotificationBase):
    pass

class NotificationInDB(IDModelMixin, DateTimeModelMixin, NotificationBase):
    pass

class NotificationPublic(IDModelMixin, DateTimeModelMixin, NotificationBase):
    pass