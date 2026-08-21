from typing import Annotated
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse

from src.api.schemas import AllowedActions, Payload, DecisionRequest
from src.config import CV_PATH
from src.services import fetch_job
from src.api.services import ApplicationService, ParsingService
from src.api.schemas import NewApplicationResponse, NewApplicationRequest
from src.models import TailoredCV
from src.services import apply_cv_edits

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

    return NewApplicationResponse(
        status=state["status"],
        id=config_id,
        interrupted=True,
        allowed_actions=[
            AllowedActions.RESUME,
            AllowedActions.EXIT,
            AllowedActions.FEEDBACK,
        ],
        payload=Payload(fit_score=state["fit_score"], fit_gaps=state["fit_gaps"], fit_rationale=state["fit_rationale"],
                        fit_recommendation=state["fit_recommendation"]),
    )


@router.get("/{id}", response_model=NewApplicationResponse, summary="Get application by id")
def get_application(id: str, service: ApplicationServiceDep):
    application = service.get_application_by_id(id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return NewApplicationResponse(
        status=application["status"],
        id=id,
        interrupted=True,
        allowed_actions=[
            AllowedActions.RESUME,
            AllowedActions.EXIT,
            AllowedActions.FEEDBACK,
        ] if application["status"] == 'awaiting_fit_approval' or application["status"] == 'cv_tailored' else [],
        payload=Payload(
            fit_score=application.get("fit_score"),
            fit_gaps=application.get("fit_gaps"),
            fit_rationale=application.get("fit_rationale"),
            fit_recommendation=application.get("fit_recommendation"),
            offer=application.get("offer"),
            cv_edits=application.get("cv_edits"),
            tailored_cv=application.get("tailored_cv"),
            tailored_cv_feedback=application.get("tailored_cv_feedback"),
            company_name=application.get("company_name"),
            company_type=application.get("company_type"),
            company_summary=application.get("company_summary"),
        ),
    )

@router.post("/{id}/decision", response_model=NewApplicationResponse, summary="Give human decision")
def decision(
        id: str,
        application_service: ApplicationServiceDep,
        request: DecisionRequest,
):
    application =  application_service.submit_decision(id,request)

    return NewApplicationResponse(
        status=application["status"],
        id=id,
        interrupted=True,
        allowed_actions=[
            AllowedActions.RESUME,
            AllowedActions.EXIT,
            AllowedActions.FEEDBACK,
        ] if application["status"] == 'awaiting_fit_approval' or application["status"] == 'cv_tailored' else [],
        payload=Payload(
            fit_score=application.get("fit_score"),
            fit_gaps=application.get("fit_gaps"),
            fit_rationale=application.get("fit_rationale"),
            fit_recommendation=application.get("fit_recommendation"),
            offer=application.get("offer"),
            cv_edits=application.get("cv_edits"),
            tailored_cv=application.get("tailored_cv"),
            tailored_cv_feedback=application.get("tailored_cv_feedback"),
            company_name=application.get("company_name"),
            company_type=application.get("company_type"),
            company_summary=application.get("company_summary"),
        ),
    )

@router.get("/{id}/cv", summary="Download tailored CV as .docx")
def get_cv(id: str, service: ApplicationServiceDep):
    application = service.get_application_by_id(id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    tailored_cv = application.get("tailored_cv")
    if tailored_cv is None:
        raise HTTPException(status_code=409, detail="Tailored CV is not ready yet")

    with NamedTemporaryFile(suffix=".docx", delete=False) as tmp_file:
        output_path = tmp_file.name

    generated_path = apply_cv_edits(CV_PATH, tailored_cv, output_path)
    with open(generated_path, "rb") as file:
        content = file.read()
    generated_path.unlink()

    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=cv_{id}.docx"},
    )