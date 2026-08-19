from dataclasses import dataclass

from fastapi import Form, UploadFile, File


@dataclass
class NewApplicationRequest:
    offer_url: str = Form(..., description="Offer URL", examples=["https://justjoin.it/job-offer/example"])
    cv: UploadFile = File(..., description="CV file (.docx)")
