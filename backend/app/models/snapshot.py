from typing import Optional
from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin

class SnapshotBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    plant_id: Optional[int]
    image_file: Optional[str]

class SnapshotCreate(SnapshotBase):
    plant_id: int
    image_file: str


class SnapshotUpdate(SnapshotBase):
    pass

class SnapshotInDB(IDModelMixin, DateTimeModelMixin, SnapshotBase):
    plant_id: int
    image_file: str

class SnapshotPublic(IDModelMixin, DateTimeModelMixin, SnapshotBase):
    plant_id: int
    image_file: str


