from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .routers.predict import router as predict_router

app = FastAPI(title="SER API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/views", StaticFiles(directory="app/views"), name="views")


@app.get("/")
def root():
    return RedirectResponse("/views/index.html")


app.include_router(predict_router, prefix="/api", tags=["Predict"])


@app.get("/healthz")
def healthz():
    return {"ok": True}
