from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.controller.perfumes_controller import router as perfumes_router
from src.middlewares.exception_middleware import ExceptionMiddleware

app = FastAPI(title="Perfume Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionMiddleware)
app.include_router(perfumes_router, prefix="/api", tags=["Perfumes"])