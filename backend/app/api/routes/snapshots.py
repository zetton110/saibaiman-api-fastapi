from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.snapshots import SnapshotsRepository
from app.models.snapshot import SnapshotCreate, SnapshotPublic
from fastapi import APIRouter, Body, Depends, HTTPException, Path, UploadFile, File
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil
import os

router = APIRouter()


@router.get('/{id}/', response_model=SnapshotPublic,
            name='snapshots:get-snapshot-by-id')
async def get_snapshot_by_id(
    id: int, snapshots_repo: SnapshotsRepository = Depends(
        get_repository(SnapshotsRepository
                       ))
) -> SnapshotPublic:
    snapshot = await snapshots_repo.get_snapshot_by_id(id=id)
    if not snapshot:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Not found')
    return snapshot

@router.get('/',
            response_model=List[SnapshotPublic],
            name='snapshots:get-all-snapshots')
async def get_all_snapshots(
    snapshots_repo: SnapshotsRepository = Depends(get_repository(SnapshotsRepository))
) -> List[SnapshotPublic]:
    return await snapshots_repo.get_all_snapshots()

@router.delete('/{id}/', response_model=int, name='snapshots:delete-snapshot-by-id')
async def delete_snapshot_by_id(
    id: int = Path(..., ge=1, title='The ID of the snapshot to delete.'),
    snapshots_repo: SnapshotsRepository = Depends(get_repository(SnapshotsRepository))
) -> int:
    snaphot = await snapshots_repo.get_snapshot_by_id(id=id)
    os.remove(f'uploads/{snaphot.image_file}')
    deleted_id = await snapshots_repo.delete_snapshot_by_id(id=snaphot.id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No snapshot found with that id.')
    return deleted_id

@router.post('/upload/image')
def uploadfile(upload_file: UploadFile = File(...)):
    path = f'uploads/{upload_file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        'filename': upload_file.filename,
        'type': upload_file.content_type
    }

@router.post('/upload/meta',
             response_model=SnapshotPublic,
             name='snapshots:create-snapshot',
             status_code=HTTP_201_CREATED)
async def create_new_snapshot(
    new_snapshot: SnapshotCreate = Body(..., embed=True),
    snapshots_repo: SnapshotsRepository = Depends(get_repository(SnapshotsRepository)),
) -> SnapshotPublic:
    created_snapshot = await snapshots_repo.create_snapshot(new_snapshot=new_snapshot)
    return created_snapshot
