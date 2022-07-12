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
    notified_to_service: Optional[bool]
    snapshot_id: Optional[int]

class NotificationCreate(NotificationBase):
    message: str

class NotificationUpdate(CoreModel):
    plant_id: Optional[int]
    service_type: Optional[ServiceType]
    notified_to_service: Optional[bool]

class NotificationInDB(IDModelMixin, DateTimeModelMixin, NotificationBase):
    plant_id: int
    service_type: ServiceType
    notified_to_service: bool
    message: str

class NotificationPublic(IDModelMixin, DateTimeModelMixin, NotificationBase):
    message: str
