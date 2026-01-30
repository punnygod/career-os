from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db

# Import routes
from routes import roles, assessment, report, auth

# Create FastAPI app
app = FastAPI(
    title="Career OS API",
    description="Career Intelligence Platform for Tech Professionals",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(roles.router)
app.include_router(assessment.router)
app.include_router(report.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    """Initialize database and seed data on startup."""
    from seeds.seed_all import seed_all
    seed_all()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Career OS API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
