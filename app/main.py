import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import Settings
from app.repositories.catalog import Catalog
from app.repositories.json_repository import DataSourceError

from app.ui import router as ui_router
from app.chat import ConversationEngine, router as chat_router
from app.api import router
from app.services.catalog_service import CatalogService, DomainError
from app.services.state import StateStore

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        application.state.catalog = None
        try:
            application.state.catalog = Catalog.load(settings.data_dir)
            application.state.service = CatalogService(application.state.catalog)
            application.state.store = StateStore(settings.database_path, application.state.service)
            application.state.store.chat = ConversationEngine(application.state.store, settings.reference_date)
        except DataSourceError:
            logger.error("Mock datasets could not be loaded")
        yield

    application = FastAPI(title=settings.application_name, lifespan=lifespan)

    application.include_router(router)
    application.include_router(chat_router)
    application.include_router(ui_router)

    @application.exception_handler(DomainError)
    async def domain_error(request: Request, exc: DomainError):
        return JSONResponse(status_code=exc.status, content={"message": exc.message})

    @application.get("/health")
    def health(request: Request):
        catalog = request.app.state.catalog
        if catalog is None:
            return JSONResponse(status_code=503, content={
                "status": "unavailable", "message": "Mock datasets are unavailable."
            })
        return {"status": "ok", "phase": 1, "stage": 4,
                "reference_date": settings.reference_date.isoformat(),
                "datasets": catalog.counts()}

    return application


app = create_app()
