from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.notification_settings import NotificationSettingsRepository
from app.models.notification_setting import NotificationSettingCreate, NotificationSettingPublic
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/all',
            response_model=List[NotificationSettingPublic],
            name='notification_settings:get-all-notification_settings')
async def get_all_notification_settings(
    notification_settings_repo: NotificationSettingsRepository = Depends(get_repository(NotificationSettingsRepository))
) -> List[NotificationSettingPublic]:
    return await notification_settings_repo.get_all_notification_settings()

@router.get('/',
            response_model=List[NotificationSettingPublic],
            name='notification_settings:get-all-notification_settings-by-plant-id')
async def get_all_notification_settings_by_plant_id(
    plant_id: int,
    notification_settings_repo: NotificationSettingsRepository = Depends(get_repository(NotificationSettingsRepository))
) -> List[NotificationSettingPublic]:
    return await notification_settings_repo.get_all_notification_settings_by_plant_id(plant_id=plant_id)

@router.post('/',
             response_model=NotificationSettingPublic,
             name='notification_settings:create-notification_setting',
             status_code=HTTP_201_CREATED)
async def create_new_notification_setting(
    new_notification_setting: NotificationSettingCreate = Body(..., embed=True),
    notification_settings_repo: NotificationSettingsRepository = Depends(get_repository(NotificationSettingsRepository)),
) -> NotificationSettingPublic:
    created_notification_setting = await notification_settings_repo.create_notification_setting(new_notification_setting=new_notification_setting)
    return created_notification_setting

@router.delete('/{id}/', response_model=int, name='notification_settings:delete-notification_setting-by-id')
async def delete_notification_setting_by_id(
    id: int = Path(..., ge=1, title='The ID of the notification_setting to delete.'),
    notification_settings_repo: NotificationSettingsRepository = Depends(get_repository(NotificationSettingsRepository))
) -> int:
    deleted_id = await notification_settings_repo.delete_notification_setting_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No notification_setting found with that id.')
    return deleted_id