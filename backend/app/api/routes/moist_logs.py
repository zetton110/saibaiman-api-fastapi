from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.moist_logs import MoistLogsRepository
from app.models.moist_log import MoistLogCreate, MoistLogPublic
from fastapi import APIRouter, Body, Depends, HTTPException, Path, UploadFile, File
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/all',
            response_model=List[MoistLogPublic],
            name='moist_logs:get-all-moist_logs')
async def get_all_moist_logs(
    moist_logs_repo: MoistLogsRepository = Depends(get_repository(MoistLogsRepository))
) -> List[MoistLogPublic]:
    return await moist_logs_repo.get_all_moist_logs()

@router.get('/',
            response_model=List[MoistLogPublic],
            name='moist_logs:get-all-moist_logs-by-plant-id')
async def get_all_moist_logs_by_plant_id(
    plant_id: int,
    moist_logs_repo: MoistLogsRepository = Depends(get_repository(MoistLogsRepository))
) -> List[MoistLogPublic]:
    return await moist_logs_repo.get_all_moist_logs_by_plant_id(plant_id=plant_id)

@router.post('/',
             response_model=MoistLogPublic,
             name='moist_logs:create-moist_log',
             status_code=HTTP_201_CREATED)
async def create_new_moist_log(
    new_moist_log: MoistLogCreate = Body(..., embed=True),
    moist_logs_repo: MoistLogsRepository = Depends(get_repository(MoistLogsRepository)),
) -> MoistLogPublic:
    created_moist_log = await moist_logs_repo.create_moist_log(new_moist_log=new_moist_log)
    return created_moist_log

@router.get('/{id}/', response_model=MoistLogPublic,
            name='moist_logs:get-moist_log-by-id')
async def get_moist_log_by_id(
    id: int, moist_logs_repo: MoistLogsRepository = Depends(
        get_repository(MoistLogsRepository
                       ))
) -> MoistLogPublic:
    moist_log = await moist_logs_repo.get_moist_log_by_id(id=id)
    if not moist_log:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Not found')
    return moist_log

@router.delete('/{id}/', response_model=int, name='moist_logs:delete-moist_log-by-id')
async def delete_moist_log_by_id(
    id: int = Path(..., ge=1, title='The ID of the moist_log to delete.'),
    moist_logs_repo: MoistLogsRepository = Depends(get_repository(MoistLogsRepository))
) -> int:
    deleted_id = await moist_logs_repo.delete_moist_log_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No moist_log found with that id.')
    return deleted_id