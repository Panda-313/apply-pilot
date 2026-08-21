from typing import Annotated, Any, Mapping
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from src.api.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from src.api.schemas import AllowedActions, Payload, DecisionRequest
from src.config import CV_PATH
from src.api.services import ApplicationService, ParsingService
from src.api.schemas import NewApplicationResponse, NewApplicationRequest
from src.services import apply_cv_edits

router = APIRouter(
    prefix='/applications',
    tags=["applications"],
)

DECISION_ALLOWED_STATUSES = {"awaiting_fit_approval", "cv_tailored"}


def get_application_service(request: Request) -> ApplicationService:
    return request.app.state.application_service


def get_parsing_service(request: Request) -> ParsingService:
    return request.app.state.parsing_service


ApplicationServiceDep = Annotated[ApplicationService, Depends(get_application_service)]
ParsingServiceDep = Annotated[ParsingService, Depends(get_parsing_service)]

def _allowed_actions_for_status(status: str) -> list[AllowedActions]:
    if status in DECISION_ALLOWED_STATUSES:
        return [
            AllowedActions.RESUME,
            AllowedActions.EXIT,
            AllowedActions.FEEDBACK,
        ]
    return []


def _to_application_response(application_id: str, application: Mapping[str, Any]) -> NewApplicationResponse:
    return NewApplicationResponse(
        status=application["status"],
        id=application_id,
        interrupted=True,
        allowed_actions=_allowed_actions_for_status(application["status"]),
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
    offer_result = parsing_service.fetch_offer(request.offer_url)
    structured_offer = parsing_service.parse_offer(offer_result)

    state, config_id = application_service.create_application(structured_cv, structured_offer)

    return _to_application_response(config_id, state)


@router.get("/{id}", response_model=NewApplicationResponse, summary="Get application by id")
def get_application(id: str, service: ApplicationServiceDep):
    application = service.get_application_by_id(id)

    if application is None:
        raise NotFoundError(
            code="application_not_found",
            message=f"Application '{id}' was not found.",
        )

    return _to_application_response(id, application)

@router.post("/{id}/decision", response_model=NewApplicationResponse, summary="Give human decision")
def decision(
        id: str,
        application_service: ApplicationServiceDep,
        request: DecisionRequest,
):
    current_application = application_service.get_application_by_id(id)
    if current_application is None:
        raise NotFoundError(
            code="application_not_found",
            message=f"Application '{id}' was not found.",
        )

    if current_application["status"] not in DECISION_ALLOWED_STATUSES:
        raise ConflictError(
            code="decision_not_allowed",
            message=f"Application '{id}' does not currently accept decisions.",
            details={"status": current_application["status"]},
        )

    if request.action == AllowedActions.FEEDBACK and not request.feedback.strip():
        raise UnprocessableEntityError(
            code="feedback_required",
            message="Feedback text is required when action is 'feedback'.",
        )

    application = application_service.submit_decision(id, request)
    if application is None:
        raise NotFoundError(
            code="application_not_found",
            message=f"Application '{id}' was not found.",
        )

    return _to_application_response(id, application)

@router.get("/{id}/cv", summary="Download tailored CV as .docx")
def get_cv(id: str, service: ApplicationServiceDep):
    application = service.get_application_by_id(id)

    if application is None:
        raise NotFoundError(
            code="application_not_found",
            message=f"Application '{id}' was not found.",
        )

    tailored_cv = application.get("tailored_cv")
    if tailored_cv is None:
        raise ConflictError(
            code="tailored_cv_not_ready",
            message="Tailored CV is not ready yet.",
        )

    with NamedTemporaryFile(suffix=".docx", delete=False) as tmp_file:
        output_path = tmp_file.name

    generated_path = apply_cv_edits(CV_PATH, tailored_cv, output_path)
    try:
        with open(generated_path, "rb") as file:
            content = file.read()
    finally:
        generated_path.unlink(missing_ok=True)

    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=cv_{id}.docx"},
    )