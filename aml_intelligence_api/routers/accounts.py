from datetime import datetime

from pydantic import BaseModel, Field


class Account(BaseModel):
    """A customer account monitored for suspicious activity."""

    account_id: int = Field(gt=0)
    customer_name: str = Field(min_length=1)
    customer_type: str = Field(min_length=1)
    country: str = Field(min_length=1)
    risk_level: str = Field(min_length=1)
    status: str = Field(min_length=1)
    # Links to Analyst. None means the account has not been assigned yet.
    analyst_id: int | None = Field(default=None, gt=0)
    opened_at: datetime
