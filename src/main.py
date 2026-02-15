import uvicorn
from fastapi import FastAPI
from api.cv_routes import router as cv_router
from api.ats_routes import router as ats_router
from core.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI instance
app = FastAPI(title=settings.app_name)

# Include Routers
app.include_router(cv_router, prefix="/api", tags=["CV Generation"])
app.include_router(ats_router, prefix="/api", tags=["ATS Analysis"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Shared CV & ATS API",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
