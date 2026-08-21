from dotenv import load_dotenv
load_dotenv()

from src.api.services.parsing_service import ParsingService


from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.exceptions import ApiError
from src.api.services import ApplicationService
from langgraph.checkpoint.memory import InMemorySaver

from src.api.routers import applications_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpointer = InMemorySaver()
    app.state.application_service = ApplicationService(checkpointer = checkpointer)
    app.state.parsing_service = ParsingService()

    try:
        yield
    finally:
        pass


app = FastAPI(
    title="Apply Pilot API",
    description="API for matching CV to given offer",
    version="0.1.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications_router)


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError):
    payload = {
        "error": {
            "code": exc.code,
            "message": exc.message,
        }
    }
    if exc.details is not None:
        payload["error"]["details"] = exc.details

    return JSONResponse(status_code=exc.status_code, content=payload)

@app.get(
    "/health",
    tags=["health"],
    summary="Health check"
)
def health_check():
    return {"status": "healthy"}
