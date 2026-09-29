from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/people", tags=["people"])


class NewPerson(BaseModel):
    name: str
    role: str
    firm_id: int


PEOPLE = [
    {"id": 1, "name": "Nadia Farouk", "role": "Associate", "firm_id": 1},
    {"id": 2, "name": "James Cole", "role": "Partner", "firm_id": 2},
]

@router.get("")
def list_people():
    return PEOPLE


@router.post("", status_code=201)
def add_person(new: NewPerson):
    person = {
        "id": len(PEOPLE) + 1,
        "name": new.name,
        "role": new.role,
        "firm_id": new.firm_id,
    }
    PEOPLE.append(person)
    return person
