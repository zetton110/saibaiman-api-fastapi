from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from app.core import config, tasks
from app.api.routes import router as api_router
import subprocess

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()

@app.on_event("startup")
@repeat_every(seconds=60, wait_first=False)
def typetalk():
    res = subprocess.run(['python','batch/notify_external_service.py', 'TYPETALK'])
    print(res.stdout)

@app.on_event("startup")
@repeat_every(seconds=60*30, wait_first=False)
def twitter():
    res = subprocess.run(['python','batch/notify_external_service.py', 'TWITTER'])
    print(res.stdout)
