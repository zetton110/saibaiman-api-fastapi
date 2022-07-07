from typing import List

from app.db.repositories.base import BaseRepository
from app.models.pump_setting import PumpSettingCreate, PumpSettingInDB
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.pump_settings as query

class PumpSettingsRepository(BaseRepository):
    async def create_pump_setting(self, *, new_pump_setting: PumpSettingCreate) -> PumpSettingInDB:
        query_values = new_pump_setting.dict()
        pump_setting = await self.db.fetch_one(
            query=query.CREATE_PUMP_SETTING_LOG_QUERY,
            values=query_values
        )
        return PumpSettingInDB(**pump_setting)

    async def get_pump_setting_by_id(self, *, id: int) -> PumpSettingInDB:
        pump_setting = await self.db.fetch_one(
            query=query.GET_PUMP_SETTING_LOG_BY_QUERY,
            values={'id': id}
        )
        if not pump_setting:
            return None
        return PumpSettingInDB(**pump_setting)

    async def get_all_pump_settings(self) -> List[PumpSettingInDB]:
        pump_setting_records = await self.db.fetch_all(
            query=query.GET_ALL_PUMP_SETTING_LOGS_QUERY)
        return [PumpSettingInDB(**item) for item in pump_setting_records]
    
    async def delete_pump_setting_by_id(self, *, id: int) -> int:
        pump_setting = await self.get_pump_setting_by_id(id=id)
        if not pump_setting:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_PUMP_SETTING_LOG_BY_ID_QUERY, values={'id': id})
        return deleted_id