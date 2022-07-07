from fastapi import APIRouter
from app.api.routes.hedgehogs import router as hedgehogs_router
from app.api.routes.plants import router as plants_router
from app.api.routes.snapshots import router as snapshots_router


router = APIRouter()
router.include_router(hedgehogs_router, prefix="/hedgehogs", tags=["hedgehogs"])
router.include_router(plants_router, prefix="/plants", tags=["plants"])
router.include_router(snapshots_router, prefix="/snapshots", tags=["snapshots"])
