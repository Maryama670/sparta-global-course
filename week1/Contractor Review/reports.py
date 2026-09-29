"""Reports API — handed over by a contractor. Not reviewed.

SYNTHETIC PLACEHOLDER DATA ONLY.
"""

import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/reports", tags=["reports"])


REPORTS: list[dict[str, Any]] = [
    {"id": 1, "title": "UK Market Outlook", "firm_id": 1, "revisions": ["v1"]},
    {"id": 2, "title": "US Partner Compensation", "firm_id": 2, "revisions": ["v1"]},
]

_view_counts: dict[int, int] = {}


class NewReport(BaseModel):
    title: str = Field(min_length=1)
    firm_id: int


def get_report_or_404(report_id: int) -> dict:
    for report in REPORTS:
        if report["id"] == report_id:
            return report
    raise HTTPException(status_code=404, detail=f"No report with id {report_id}")


@router.get("")
def list_reports():
    return REPORTS


@router.get("/{report_id}")
def get_report(report_id: int):
    report = get_report_or_404(report_id)#$ curl http://localhost:8000/reports/1 returns +1 entry
    _view_counts[report_id] = _view_counts.get(report_id, 0) + 1 #plus 1 id generated unsafely 1+1=2+1=etc
    return {**report, "views": _view_counts[report_id]}


@router.post("", status_code=201)
def create_report(new: NewReport):#before new firm id is created check if it exist
    new_id = max(report["id"] for report in REPORTS) + 1
    report = {  
        "id": new_id,
        "title": new.title,
        "firm_id": new.firm_id,
        "revisions": ["v1"],
    }
    REPORTS.append(report)
    return report


@router.put("/{report_id}")
def update_report(report_id: int, new: NewReport):
    report = get_report_or_404(report_id)
    report["title"] = new.title
    report["firm_id"] = new.firm_id
    report["revisions"].append(f"v{len(report['revisions']) + 1}") #plus 1 id report retry again issue not safe
    return report


@router.get("/{report_id}/export")
async def export_report(report_id: int):
    report = get_report_or_404(report_id)
    await time.sleep(10) #change from 3 to 10 see performance #1
    return {"id": report["id"], "title": report["title"], "format": "pdf"}


@router.delete("/{report_id}", status_code=204)
def delete_report(report_id: int):
    report = get_report_or_404(report_id)
    REPORTS.remove(report)
    return


# 1. export_report blocking the event loop
# 2. create_report is not validating firm_id and has a race condition if two requests come in at the same time
# 3. update_report mutating the state in retries and it’s not idempotent
# 4. get_report mutating the state and it’s not idempotent