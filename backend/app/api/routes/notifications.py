from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.notifications import NotificationsRepository
from app.models.notification import NotificationCreate, NotificationPublic, ServiceType
from fastapi import APIRouter, Body, Depends, HTTPException, Path, UploadFile, File
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/all',
            response_model=List[NotificationPublic],
            name='notifications:get-all-notifications')
async def get_all_notifications(
    notifications_repo: NotificationsRepository = Depends(get_repository(NotificationsRepository))
) -> List[NotificationPublic]:
    return await notifications_repo.get_all_notifications()

@router.get('/',
            response_model=List[NotificationPublic],
            name='notifications:get-all-notifications-by-plant-id')
async def get_all_notifications_by_plant_id(
    plant_id: int,
    notifications_repo: NotificationsRepository = Depends(get_repository(NotificationsRepository))
) -> List[NotificationPublic]:
    return await notifications_repo.get_all_notifications_by_plant_id(plant_id=plant_id)

@router.get('/latest-one',
            response_model=NotificationPublic,
            name='notifications:get-latest-notification-by-plant-id-and-service-type')
async def get_latest_notification_by_plant_id_and_service_type(
    plant_id: int,
    service_type: ServiceType,
    notifications_repo: NotificationsRepository = Depends(get_repository(NotificationsRepository))
) -> NotificationPublic:
    return await notifications_repo.get_latest_notification_by_plant_id_and_service_type(plant_id=plant_id, service_type= service_type)

@router.post('/',
             response_model=NotificationPublic,
             name='notifications:create-notification',
             status_code=HTTP_201_CREATED)
async def create_new_notification(
    new_notification: NotificationCreate = Body(..., embed=True),
    notifications_repo: NotificationsRepository = Depends(get_repository(NotificationsRepository)),
) -> NotificationPublic:
    created_notification = await notifications_repo.create_notification(new_notification=new_notification)
    return created_notification

@router.delete('/{id}/', response_model=int, name='notifications:delete-notification-by-id')
async def delete_notification_by_id(
    id: int = Path(..., ge=1, title='The ID of the notification to delete.'),
    notifications_repo: NotificationsRepository = Depends(get_repository(NotificationsRepository))
) -> int:
    deleted_id = await notifications_repo.delete_notification_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No notification found with that id.')
    return deleted_id