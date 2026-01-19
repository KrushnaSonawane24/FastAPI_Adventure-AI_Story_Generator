from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import story, job
from DB.database import create_tables

# Import models so they register with Base
from models import job as job_model, story as story_model

create_tables()

app = FastAPI(
    title="choose youre adventure Game API",
    description="api genrate cool stories",
    docs_url="/docs",redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],#this use full for the get post put update methods 
    allow_headers=["*"])

app.include_router(story.router,prefix=settings.API_PREFIX)
app.include_router(job.router,prefix=settings.API_PREFIX)

@app.get("/")
def get_function():
    return {"message": "Interactive Story Generator API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment (Render/Choreo sets this) or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=port
    )
