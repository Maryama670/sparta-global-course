from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Alert(BaseModel):
    """A warning that transaction activity triggered a detection rule."""

    alert_id: int = Field(gt=0)
    account_id: int = Field(gt=0)  # Links to Account.
    transaction_id: int = Field(gt=0)  # Links to Transaction.
    rule_id: int = Field(gt=0)  # Look up the rule instead of repeating its name.
    amount: Decimal = Field(gt=0)
    corridor: str = Field(min_length=1)
    score: int = Field(ge=0, le=100)
    status: str = Field(min_length=1)
    created_at: datetime
