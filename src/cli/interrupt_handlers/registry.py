from typing import Callable

from .fit_analyst_approval import handle_fit_analyst_approval
from .cv_tailor_approval import handle_cv_tailor_approval


INTERRUPT_HANDLERS: dict[str, Callable[[dict], dict]] = {
    "fit_analyst_approval": handle_fit_analyst_approval,
    "cv_tailor_approval": handle_cv_tailor_approval,
}


def handle_interrupt(interrupt_value: dict) -> dict:
    interrupt_type = interrupt_value.get("type")
    
    if not interrupt_type:
        raise ValueError("Interrupt value missing 'type' field")
    
    handler = INTERRUPT_HANDLERS.get(interrupt_type)
    
    if not handler:
        raise ValueError(f"Unknown interrupt type: {interrupt_type}")
    
    return handler(interrupt_value)
