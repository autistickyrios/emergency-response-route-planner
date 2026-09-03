from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router as routes_router
from backend.app.api.incidents import router as incidents_router

from backend.app.api.ambulances import (
    router as ambulances_router,
)

from backend.app.api.dispatch import (
    router as dispatch_router,
)

from backend.app.api.hospitals import (
    router as hospitals_router,
)

from backend.app.api.response import (
    router as response_router,
)

from backend.app.api.lifecycle import (
    router as lifecycle_router,
)

app = FastAPI(
    title="Emergency Response Route Planner",
    description="AI-powered emergency response routing system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_router)
app.include_router(incidents_router)
app.include_router(ambulances_router)
app.include_router(dispatch_router)
app.include_router(hospitals_router)
app.include_router(response_router)
app.include_router(lifecycle_router)



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