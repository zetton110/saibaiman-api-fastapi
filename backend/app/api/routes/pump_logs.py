from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.pump_logs import PumpLogsRepository
from app.models.pump_log import PumpLogCreate, PumpLogPublic
from fastapi import APIRouter, Body, Depends, HTTPException, Path, UploadFile, File
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/',
            response_model=List[PumpLogPublic],
            name='pump_logs:get-all-pump_logs')
async def get_all_pump_logs(
    pump_logs_repo: PumpLogsRepository = Depends(get_repository(PumpLogsRepository))
) -> List[PumpLogPublic]:
    return await pump_logs_repo.get_all_pump_logs()

@router.post('/',
             response_model=PumpLogPublic,
             name='pump_logs:create-pump_log',
             status_code=HTTP_201_CREATED)
async def create_new_pump_log(
    new_pump_log: PumpLogCreate = Body(..., embed=True),
    pump_logs_repo: PumpLogsRepository = Depends(get_repository(PumpLogsRepository)),
) -> PumpLogPublic:
    created_pump_log = await pump_logs_repo.create_pump_log(new_pump_log=new_pump_log)
    return created_pump_log

@router.get('/{id}/', response_model=PumpLogPublic,
            name='pump_logs:get-pump_log-by-id')
async def get_pump_log_by_id(
    id: int, pump_logs_repo: PumpLogsRepository = Depends(
        get_repository(PumpLogsRepository
                       ))
) -> PumpLogPublic:
    pump_log = await pump_logs_repo.get_pump_log_by_id(id=id)
    if not pump_log:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Not found')
    return pump_log

@router.delete('/{id}/', response_model=int, name='pump_logs:delete-pump_log-by-id')
async def delete_pump_log_by_id(
    id: int = Path(..., ge=1, title='The ID of the pump_log to delete.'),
    pump_logs_repo: PumpLogsRepository = Depends(get_repository(PumpLogsRepository))
) -> int:
    deleted_id = await pump_logs_repo.delete_pump_log_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No pump_log found with that id.')
    return deleted_id