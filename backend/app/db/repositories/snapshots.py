from typing import List

from app.db.repositories.base import BaseRepository
from app.models.snapshot import SnapshotCreate, SnapshotInDB
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import app.db.repositories.queries.snapshots as query

class SnapshotsRepository(BaseRepository):
    async def create_snapshot(self, *, new_snapshot: SnapshotCreate) -> SnapshotInDB:
        query_values = new_snapshot.dict()
        snapshot = await self.db.fetch_one(
            query=query.CREATE_SNAPSHOT_QUERY,
            values=query_values
        )
        return SnapshotInDB(**snapshot)
    
    async def get_snapshot_by_id(self, *, id: int) -> SnapshotInDB:
        snapshot = await self.db.fetch_one(
            query=query.GET_SNAPSHOT_BY_ID_QUERY,
            values={'id': id}
        )
        if not snapshot:
            return None
        return SnapshotInDB(**snapshot)

    async def get_all_snapshots(self) -> List[SnapshotInDB]:
        snapshot_records = await self.db.fetch_all(
            query=query.GET_ALL_SNAPSHOTS_QUERY)
        return [SnapshotInDB(**item) for item in snapshot_records]
    
    async def delete_snapshot_by_id(self, *, id: int) -> int:
        snapshot = await self.get_snapshot_by_id(id=id)
        if not snapshot:
            return None
        deleted_id = await self.db.execute(
            query=query.DELETE_SNAPSHOT_BY_ID_QUERY, values={'id': id})
        return deleted_id