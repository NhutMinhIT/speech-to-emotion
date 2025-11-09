from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.predict import router as predict_router

app = FastAPI(title="SER API", version="2.0")

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # đổi sang domain FE 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(predict_router, prefix="/api", tags=["Predict"])


# healthcheck
@app.get("/healthz")
def healthz():
    return {"ok": True}
