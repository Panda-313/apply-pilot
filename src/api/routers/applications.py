from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException

from src import State
from src.services import fetch_job
from src.api.services import ApplicationService, ParsingService
from src.api.schemas import NewApplicationResponse, NewApplicationRequest

router = APIRouter(
    prefix='/applications',
    tags=["applications"],
)


def get_application_service(request: Request) -> ApplicationService:
    return request.app.state.application_service


def get_parsing_service(request: Request) -> ParsingService:
    return request.app.state.parsing_service


ApplicationServiceDep = Annotated[ApplicationService, Depends(get_application_service)]
ParsingServiceDep = Annotated[ParsingService, Depends(get_parsing_service)]


@router.post(
    "",
    response_model=NewApplicationResponse,
    status_code=201,
    summary="Create a new application",
    description="Create new application to match cv to the given offer",
)
def create_application(
        parsing_service: ParsingServiceDep,
        application_service: ApplicationServiceDep,
        request: NewApplicationRequest = Depends(),
):
    structured_cv = parsing_service.parse_cv(request.cv)
    structured_offer = parsing_service.parse_offer(
        fetch_job(request.offer_url),
    )

    state, config_id = application_service.create_application(structured_cv, structured_offer)

    return NewApplicationResponse(status=state["status"], id=config_id)


@router.get("/{id}", response_model=State, summary="Get application by id")
def get_application(id: str, service: ApplicationServiceDep):
    application = service.get_application_by_id(id)
    
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application

