from typing import List

from app.db.repositories.base import BaseRepository
from app.models.notification import NotificationCreate, NotificationInDB, ServiceType
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.notifications as query

class NotificationsRepository(BaseRepository):
    async def create_notification(self, *, new_notification: NotificationCreate) -> NotificationInDB:
        query_values = new_notification.dict()
        notification = await self.db.fetch_one(
            query=query.CREATE_NOTIFICATION_QUERY,
            values=query_values
        )
        return NotificationInDB(**notification)

    async def get_notification_by_id(self, *, id: int) -> NotificationInDB:
        notification = await self.db.fetch_one(
            query=query.GET_NOTIFICATION_BY_ID_QUERY,
            values={'id': id}
        )
        if not notification:
            return None
        return NotificationInDB(**notification)

    async def get_latest_notification_by_plant_id_and_service_type(self, *, plant_id: int, service_type: ServiceType) -> NotificationInDB:
        notification = await self.db.fetch_one(
            query=query.GET_LATEST_NOTIFICATION_BY_PLANT_ID_AND_SERVICE_TYPE_QUERY,
            values={'plant_id': plant_id, 'service_type': service_type}
        )
        if not notification:
            return None
        return NotificationInDB(**notification)

    async def get_all_notifications(self) -> List[NotificationInDB]:
        notification_records = await self.db.fetch_all(
            query=query.GET_ALL_NOTIFICATIONS_QUERY)
        return [NotificationInDB(**item) for item in notification_records]
    
    async def get_all_notifications_by_plant_id(self, *, plant_id: int) -> List[NotificationInDB]:
        notification_records = await self.db.fetch_all(
            query=query.GET_ALL_NOTIFICATIONS_QUERY_BY_PLANT_ID,
            values={'plant_id': plant_id})
        return [NotificationInDB(**item) for item in notification_records]
    
    async def delete_notification_by_id(self, *, id: int) -> int:
        notification = await self.get_notification_by_id(id=id)
        if not notification:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_NOTIFICATION_BY_ID_QUERY, values={'id': id})
        return deleted_id