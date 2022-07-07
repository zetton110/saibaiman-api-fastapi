from fastapi import APIRouter
from app.api.routes.hedgehogs import router as hedgehogs_router
from app.api.routes.plants import router as plants_router
from app.api.routes.snapshots import router as snapshots_router
from app.api.routes.moist_logs import router as moist_logs_router
from app.api.routes.pump_logs import router as pump_logs_router
from app.api.routes.pump_settings import router as pump_settings_router

router = APIRouter()
router.include_router(hedgehogs_router, prefix="/hedgehogs", tags=["hedgehogs"])
router.include_router(plants_router, prefix="/plants", tags=["plants"])
router.include_router(snapshots_router, prefix="/snapshots", tags=["snapshots"])
router.include_router(moist_logs_router, prefix="/moist_logs", tags=["moist_logs"])
router.include_router(pump_logs_router, prefix="/pump_logs", tags=["pump_logs"])
router.include_router(pump_settings_router, prefix="/pump_settings", tags=["pump_settings"])
