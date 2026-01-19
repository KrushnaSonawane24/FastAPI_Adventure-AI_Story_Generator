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
    return {"message":"hello there how are you "}

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    from threading import Timer
    
    # Browser 2 seconds baad open hoga
    Timer(2, lambda: webbrowser.open("http://localhost:8000")).start()
    
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
