from .not_trasformed_offer import FetchJobSuccess, FetchJobResult, FetchJobFailed
from .company_type import CompanyType
from .fit_recommendation import FitRecommendation
from .state_status import StateStatus
from .structured_offer import StructuredOffer
from .structured_cv import StructuredCV, TailoredCV
from .clarifications import Clarifications, SkillYears

__all__ = [
    'FetchJobSuccess',
    'StructuredOffer',
    'FetchJobFailed',
    'FetchJobResult',
    'CompanyType',
    'FitRecommendation',
    'StateStatus',
    'StructuredCV',
    'TailoredCV',
    'Clarifications',
    'SkillYears',
]
