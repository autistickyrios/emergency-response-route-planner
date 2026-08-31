from fastapi import FastAPI

from backend.app.api.routes import router as routes_router
from backend.app.api.incidents import router as incidents_router


app = FastAPI(
    title="Emergency Response Route Planner",
    description="AI-powered emergency response routing system",
    version="1.0.0",
)

app.include_router(routes_router)
app.include_router(incidents_router)


@app.get("/")
def root():
    return {
        "name": "Emergency Response Route Planner",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}