from typing import TypedDict

from src.models import FetchJobSuccess


class State(TypedDict):
    not_transformed_offer: FetchJobSuccess
