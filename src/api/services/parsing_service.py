from docx import Document
from fastapi import UploadFile

from src.models import FetchJobResult, FetchJobSuccess, StructuredCV, StructuredOffer
from src.services import parse_cv, fetch_job
from src.services.parse_offer import parse_offer


class ParsingService:
    def parse_cv(self, cv: UploadFile) -> StructuredCV:
        doc = Document(cv.file)
        return parse_cv(doc)

    def parse_offer(self, job_result: FetchJobSuccess) -> StructuredOffer:
        return parse_offer(job_result)

    def fetch_offer(self, url: str) -> FetchJobResult:
        return fetch_job(url)