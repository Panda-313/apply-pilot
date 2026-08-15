from typing import TypedDict

from models import FetchJobSuccess


class State(TypedDict):
    not_transformed_offer: FetchJobSuccess
