from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that handles startup and shutdown logic.
    Creates database tables automatically on startup.
    """
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Notes REST API",
    description="A simple, production-ready Notes REST API built with FastAPI, SQLAlchemy, and Pydantic.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS Middleware (allows requests from frontends if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(notes.router)


@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint providing API information and documentation link.
    """
    return {
        "message": "Welcome to the Notes REST API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "healthy",
    }
