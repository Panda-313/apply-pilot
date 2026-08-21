from typing import cast
from zipfile import BadZipFile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from fastapi import UploadFile

from src.api.exceptions import (
    ApiError,
    BadRequestError,
    UnprocessableEntityError,
    UpstreamServiceError,
)
from src.models import FetchJobResult, FetchJobSuccess, StructuredCV, StructuredOffer
from src.services import parse_cv, fetch_job
from src.services.parse_offer import parse_offer


class ParsingService:
    def parse_cv(self, cv: UploadFile) -> StructuredCV:
        filename = (cv.filename or "").lower()
        if not filename.endswith(".docx"):
            raise UnprocessableEntityError(
                code="invalid_cv_file_type",
                message="CV file must be a .docx document.",
            )

        try:
            doc = Document(cv.file)
        except (PackageNotFoundError, BadZipFile, ValueError):
            raise UnprocessableEntityError(
                code="invalid_cv_file",
                message="Provided CV file is not a valid .docx document.",
            )

        return parse_cv(doc)

    def parse_offer(self, job_result: FetchJobResult) -> StructuredOffer:
        if job_result["status"] == "failed":
            raise self._map_fetch_error(job_result["error"], job_result["source_url"])

        return parse_offer(cast(FetchJobSuccess, job_result))

    def fetch_offer(self, url: str) -> FetchJobResult:
        return fetch_job(url)

    def _map_fetch_error(self, error_code: str, source_url: str) -> ApiError:
        details = {"source_url": source_url, "fetch_error": error_code}

        if error_code == "invalid_url":
            return BadRequestError(
                code="invalid_offer_url",
                message="Offer URL is invalid. Provide a valid http/https URL.",
                details=details,
            )

        if error_code in {"empty_content", "not_html", "js_heavy_suspected"}:
            return UnprocessableEntityError(
                code="unreadable_offer_content",
                message="Could not extract readable offer content from the provided URL.",
                details=details,
            )

        return UpstreamServiceError(
            code="offer_fetch_failed",
            message="Could not fetch the offer from the external website.",
            details=details,
        )