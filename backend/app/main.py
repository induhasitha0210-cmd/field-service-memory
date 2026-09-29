import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.routers import (
    customers,
    demo,
    equipment,
    insights,
    memory,
    service_requests,
    sites,
    technicians,
)
from app.services.hindsight_service import hindsight_service
from app.services.seed_service import SeedService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("field_service_memory")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed demo data
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        SeedService.seed_all(db)
    except Exception as exc:
        logger.error("Error during initial data seeding: %s", exc)
    finally:
        db.close()

    hindsight_stat = hindsight_service.get_status()
    logger.info(
        "Memory Engine status: %s (bank=%s)",
        hindsight_stat.get("mode"),
        hindsight_stat.get("bank_id"),
    )
    yield
    logger.info("Shutting down Field Service Memory backend.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api
app.include_router(service_requests.router, prefix="/api")
app.include_router(equipment.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(sites.router, prefix="/api")
app.include_router(technicians.router, prefix="/api")
app.include_router(memory.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(demo.router, prefix="/api")


@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "tagline": "The Technician Who Never Forgets",
        "version": settings.VERSION,
        "docs": "/docs",
        "hindsight": hindsight_service.get_status(),
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "hindsight": hindsight_service.get_status(),
    }
