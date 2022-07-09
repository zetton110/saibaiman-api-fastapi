from typing import List

from app.db.repositories.base import BaseRepository
from app.models.moist_log import MoistLogCreate, MoistLogInDB
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.moist_logs as query

class MoistLogsRepository(BaseRepository):
    async def create_moist_log(self, *, new_moist_log: MoistLogCreate) -> MoistLogInDB:
        query_values = new_moist_log.dict()
        moist_log = await self.db.fetch_one(
            query=query.CREATE_MOIST_LOG_QUERY,
            values=query_values
        )
        return MoistLogInDB(**moist_log)

    async def get_moist_log_by_id(self, *, id: int) -> MoistLogInDB:
        moist_log = await self.db.fetch_one(
            query=query.GET_MOIST_LOG_BY_ID_QUERY,
            values={'id': id}
        )
        if not moist_log:
            return None
        return MoistLogInDB(**moist_log)

    async def get_all_moist_logs(self) -> List[MoistLogInDB]:
        moist_log_records = await self.db.fetch_all(
            query=query.GET_ALL_MOIST_LOGS_QUERY)
        return [MoistLogInDB(**item) for item in moist_log_records]
    
    async def delete_moist_log_by_id(self, *, id: int) -> int:
        moist_log = await self.get_moist_log_by_id(id=id)
        if not moist_log:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_MOIST_LOG_BY_ID_QUERY, values={'id': id})
        return deleted_id