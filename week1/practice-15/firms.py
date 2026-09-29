from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

router = APIRouter(prefix="/firms", tags=["firms"])

class NewFirm(BaseModel):
    name: str = Field(min_length=1)
    jurisdiction: str = Field(min_length=2)

FIRMS = [
    {"id": 1, "name": "Harding & Voss", "jurisdiction": "UK"},
    {"id": 2, "name": "Barton Legal", "jurisdiction": "US"},
]


def find_firm(firm_id: int):
    for firm in FIRMS:
        if firm["id"] == firm_id:
            return firm
    raise HTTPException(status_code=404, detail="Firm not found")


@router.get("/{firm_id}")
def get_firm(firm=Depends(find_firm)):
    return firm


@router.get("")
def list_firms(jurisdiction: str | None = None):
    if jurisdiction:
        return [firm for firm in FIRMS if firm["jurisdiction"] == jurisdiction]
    return FIRMS


@router.post("", status_code=201)
def add_firm(new: NewFirm):
    firm = {
        "id": len(FIRMS) + 1,
        "name": new.name,
        "jurisdiction": new.jurisdiction,
    }
    FIRMS.append(firm)
    return firm

@router.put("/{firm_id}")
def update_firm(firm_id: int, new: NewFirm):
    for firm in FIRMS:
        if firm["id"] == firm_id:
            firm["name"] = new.name
            firm["jurisdiction"] = new.jurisdiction
            return firm

    raise HTTPException(status_code=404, detail="Firm not found")

@router.delete("/{firm_id}", status_code=204)
def delete_firm(firm_id: int):
    for firm in FIRMS:
        if firm["id"] == firm_id:
            FIRMS.remove(firm)
            return
    raise HTTPException(status_code=404, detail="Firm not found")
