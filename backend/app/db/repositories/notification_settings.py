from typing import List

from app.db.repositories.base import BaseRepository
from app.models.notification_setting import NotificationSettingCreate, NotificationSettingInDB
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.notification_settings as query

class NotificationSettingsRepository(BaseRepository):
    async def create_notification_setting(self, *, new_notification_setting: NotificationSettingCreate) -> NotificationSettingInDB:
        query_values = new_notification_setting.dict()
        notification_setting = await self.db.fetch_one(
            query=query.CREATE_NOTIFICATION_SETTING_QUERY,
            values=query_values
        )
        return NotificationSettingInDB(**notification_setting)

    async def get_notification_setting_by_id(self, *, id: int) -> NotificationSettingInDB:
        notification_setting = await self.db.fetch_one(
            query=query.GET_NOTIFICATION_SETTING_BY_ID_QUERY,
            values={'id': id}
        )
        if not notification_setting:
            return None
        return NotificationSettingInDB(**notification_setting)

    async def get_all_notification_settings(self) -> List[NotificationSettingInDB]:
        notification_setting_records = await self.db.fetch_all(
            query=query.GET_ALL_NOTIFICATION_SETTINGS_QUERY)
        return [NotificationSettingInDB(**item) for item in notification_setting_records]

    async def get_all_notification_settings_by_plant_id(self, *, plant_id: int) -> List[NotificationSettingInDB]:
        notification_setting_records = await self.db.fetch_all(
            query=query.GET_ALL_NOTIFICATION_SETTINGS_QUERY_BY_PLANT_ID,
            values={'plant_id': plant_id})
        return [NotificationSettingInDB(**item) for item in notification_setting_records]
    
    async def delete_notification_setting_by_id(self, *, id: int) -> int:
        notification_setting = await self.get_notification_setting_by_id(id=id)
        if not notification_setting:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_NOTIFICATION_SETTING_BY_ID_QUERY, values={'id': id})
        return deleted_id