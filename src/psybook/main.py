from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from psybook.api.routes import router as api_router
from psybook.web.routes import router as web_router
from psybook.infra.db import create_db_and_tables
from fastapi.templating import Jinja2Templates

app = FastAPI(title="PsyBook", version="0.1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix="/api/v1")
app.include_router(web_router)  # <-- ВАЖНО, без prefix, значит "/"

app.mount("/static", StaticFiles(directory="src/psybook/static"), name="static")
