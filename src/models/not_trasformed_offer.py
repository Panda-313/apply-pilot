from typing import TypedDict, Literal

class FetchJobSuccess(TypedDict):
    status: Literal["success"]
    source_url: str
    title: str | None
    cleaned_text: str
    raw_html_length: int


class FetchJobFailed(TypedDict):
    status: Literal["failed"]
    source_url: str
    error: str
    title: None
    cleaned_text: None
    raw_html_length: None


FetchJobResult = FetchJobSuccess | FetchJobFailed