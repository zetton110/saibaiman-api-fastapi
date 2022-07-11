from typing import List

from app.db.repositories.base import BaseRepository
from app.models.plant import PlantCreate, PlantInDB, PlantUpdate
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.plants as query

class PlantsRepository(BaseRepository):
    async def create_plant(self, *, new_plant: PlantCreate) -> PlantInDB:
        query_values = new_plant.dict()
        plant = await self.db.fetch_one(
            query=query.CREATE_PLANT_QUERY,
            values=query_values
        )
        return PlantInDB(**plant)

    async def get_plant_by_id(self, *, id: int) -> PlantInDB:
        plant = await self.db.fetch_one(
            query=query.GET_PLANT_BY_QUERY,
            values={'id': id}
        )
        if not plant:
            return None
        return PlantInDB(**plant)
    
    async def get_all_plants(self) -> List[PlantInDB]:
        plant_records = await self.db.fetch_all(
            query=query.GET_ALL_PLANTS_QUERY)
        return [PlantInDB(**item) for item in plant_records]
    
    async def update_plant(
        self, *, id: int, plant_update: PlantUpdate
    ) -> PlantInDB:
        plant = await self.get_plant_by_id(id=id)
        if not plant:
            return None
        plant_update_params = plant.copy(
            update=plant_update.dict(exclude_unset=True))
        if plant_update_params.plant_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid plant type. Cannot be None.')
        try:
            updated_plant = await self.db.fetch_one(
                query=query.UPDATE_PLANT_BY_ID_QUERY,
                values=plant_update_params.dict(exclude={"created_at", "updated_at"})
            )
            return PlantInDB(**updated_plant)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid update params.'
            )
    
    async def delete_plant_by_id(self, *, id: int) -> int:
        plant = await self.get_plant_by_id(id=id)
        if not plant:
            return None
        deleted_id = await self.db.execute(
            query= query.DELETE_PLANT_BY_ID_QUERY, values={'id': id})
        return deleted_id
