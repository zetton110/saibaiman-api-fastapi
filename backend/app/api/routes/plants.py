from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.plants import PlantsRepository
from app.models.plant import PlantCreate, PlantPublic, PlantUpdate
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import shutil

router = APIRouter()

@router.get('/',
            response_model=List[PlantPublic],
            name='plants:get-all-plants')
async def get_all_plants(
    plants_repo: PlantsRepository = Depends(get_repository(PlantsRepository))
) -> List[PlantPublic]:
    return await plants_repo.get_all_plants()

@router.post('/',
             response_model=PlantPublic,
             name='plants:create-plant',
             status_code=HTTP_201_CREATED)
async def create_new_plant(
    new_plant: PlantCreate = Body(..., embed=True),
    plants_repo: PlantsRepository = Depends(get_repository(PlantsRepository)),
) -> PlantPublic:
    created_plant = await plants_repo.create_plant(new_plant=new_plant)
    return created_plant

@router.get('/{id}/', response_model=PlantPublic,
            name='plants:get-plant-by-id')
async def get_plant_by_id(
    id: int, plants_repo: PlantsRepository = Depends(
        get_repository(PlantsRepository
                       ))
) -> PlantPublic:
    plant = await plants_repo.get_plant_by_id(id=id)
    if not plant:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Not found')
    return plant

@router.put('/{id}/', response_model=PlantPublic,
            name='plants:update-plant-by-id')
async def update_plant_by_id(
    id: int = Path(..., ge=1, title='The ID of the plant to update.'),
    plant_update: PlantUpdate = Body(..., embed=True),
    plants_repo: PlantsRepository = Depends(get_repository(PlantsRepository)),
) -> PlantPublic:
    updated_plant = await plants_repo.update_plant(
        id=id,
        plant_update=plant_update)
    if not updated_plant:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No plant found with that id.')
    return updated_plant

@router.delete('/{id}/', response_model=int, name='plants:delete-plant-by-id')
async def delete_plant_by_id(
    id: int = Path(..., ge=1, title='The ID of the plant to delete.'),
    plants_repo: PlantsRepository = Depends(get_repository(PlantsRepository))
) -> int:
    deleted_id = await plants_repo.delete_plant_by_id(id=id)
    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='No plant found with that id.')
    return deleted_id
