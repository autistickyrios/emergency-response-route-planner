from fastapi import FastAPI

app = FastAPI(
    title="Emergency Response Route Planner",
    description="AI-powered emergency response routing system",
    version="1.0.0",
)


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