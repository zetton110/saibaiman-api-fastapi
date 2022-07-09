from typing import List

from app.db.repositories.base import BaseRepository
from app.models.pump_log import PumpLogCreate, PumpLogInDB
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.pump_logs as query

class PumpLogsRepository(BaseRepository):
    async def create_pump_log(self, *, new_pump_log: PumpLogCreate) -> PumpLogInDB:
        query_values = new_pump_log.dict()
        pump_log = await self.db.fetch_one(
            query=query.CREATE_PUMP_LOG_QUERY,
            values=query_values
        )
        return PumpLogInDB(**pump_log)

    async def get_pump_log_by_id(self, *, id: int) -> PumpLogInDB:
        pump_log = await self.db.fetch_one(
            query=query.GET_PUMP_LOG_BY_ID_QUERY,
            values={'id': id}
        )
        if not pump_log:
            return None
        return PumpLogInDB(**pump_log)

    async def get_all_pump_logs(self) -> List[PumpLogInDB]:
        pump_log_records = await self.db.fetch_all(
            query=query.GET_ALL_PUMP_LOGS_QUERY)
        return [PumpLogInDB(**item) for item in pump_log_records]
    
    async def delete_pump_log_by_id(self, *, id: int) -> int:
        pump_log = await self.get_pump_log_by_id(id=id)
        if not pump_log:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_PUMP_LOG_BY_ID_QUERY, values={'id': id})
        return deleted_id