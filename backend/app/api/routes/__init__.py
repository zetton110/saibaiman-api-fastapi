from fastapi import APIRouter
from app.api.routes.plants import router as plants_router
from app.api.routes.snapshots import router as snapshots_router
from app.api.routes.moist_logs import router as moist_logs_router
from app.api.routes.pump_logs import router as pump_logs_router
from app.api.routes.pump_settings import router as pump_settings_router
from app.api.routes.notification_settings import router as notification_settings_router
from app.api.routes.notifications import router as notifications_router

router = APIRouter()
router.include_router(plants_router, prefix="/plants", tags=["plants"])
router.include_router(snapshots_router, prefix="/snapshots", tags=["snapshots"])
router.include_router(moist_logs_router, prefix="/moist_logs", tags=["moist_logs"])
router.include_router(pump_logs_router, prefix="/pump_logs", tags=["pump_logs"])
router.include_router(pump_settings_router, prefix="/pump_settings", tags=["pump_settings"])
router.include_router(notification_settings_router, prefix="/notification_settings", tags=["notification_settings"])
router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
