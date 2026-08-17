from .not_trasformed_offer import FetchJobSuccess, FetchJobResult, FetchJobFailed
from .company_type import CompanyType
from .fit_recommendation import FitRecommendation
from .state_status import StateStatus
from .structured_cv import StructuredCV, TailoredCV

__all__ = [
    'FetchJobSuccess',
    'FetchJobFailed',
    'FetchJobResult',
    'CompanyType',
    'FitRecommendation',
    'StateStatus',
    'StructuredCV',
    'TailoredCV',
]
