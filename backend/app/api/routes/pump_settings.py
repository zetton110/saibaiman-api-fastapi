from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.pump_settings import PumpSettingsRepository
from app.models.pump_setting import PumpSettingCreate, PumpSettingPublic
from fastapi import APIRouter, Body, Depends, HTTPException, Path, UploadFile, File
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/all',
            response_model=List[PumpSettingPublic],
            name='pump_settings:get-all-pump_settings')
async def get_all_pump_settings(
    pump_settings_repo: PumpSettingsRepository = Depends(get_repository(PumpSettingsRepository))
) -> List[PumpSettingPublic]:
    return await pump_settings_repo.get_all_pump_settings()

@router.post('/',
             response_model=PumpSettingPublic,
             name='pump_settings:create-pump_setting',
             status_code=HTTP_201_CREATED)
async def create_new_pump_setting(
    new_pump_setting: PumpSettingCreate = Body(..., embed=True),
    pump_settings_repo: PumpSettingsRepository = Depends(get_repository(PumpSettingsRepository)),
) -> PumpSettingPublic:
    created_pump_setting = await pump_settings_repo.create_pump_setting(new_pump_setting=new_pump_setting)
    return created_pump_setting

@router.get('/', response_model=PumpSettingPublic,
            name='pump_settings:get-pump_setting-by-id')
async def get_pump_setting_by_with_query_params(
    plant_id: int, pump_settings_repo: PumpSettingsRepository = Depends(
        get_repository(PumpSettingsRepository
                       ))
) -> PumpSettingPublic:
    pump_setting = await pump_settings_repo.get_pump_setting_by_plant_id(plant_id=plant_id)
    if not pump_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Not found')
    return pump_setting

@router.delete('/{id}/', response_model=int, name='pump_settings:delete-pump_setting-by-id')
async def delete_pump_setting_by_id(
    id: int = Path(..., ge=1, title='The ID of the pump_setting to delete.'),
    pump_settings_repo: PumpSettingsRepository = Depends(get_repository(PumpSettingsRepository))
) -> int:
    deleted_id = await pump_settings_repo.delete_pump_setting_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No pump_setting found with that id.')
    return deleted_id