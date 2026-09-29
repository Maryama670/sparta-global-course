from fastapi import APIRouter, Depends, HTTPException  # Import APIRouter to group routes, Depends to resolve dependencies and HTTPException to return errors.
from pydantic import BaseModel, Field  # Import BaseModel for validated data schemas and Field for field constraints and descriptions.

from data import PEOPLE  # Import the shared in-memory list of person records.
from routers.firms import get_firm_or_404  # Import the helper that finds a firm by ID or raises an HTTP 404 error.

router = APIRouter(prefix="/people", tags=["people"])  # Group these endpoints under the configured URL prefix and documentation tag.


# name
# role
# firm_id
class NewPerson(BaseModel):  # Define the validated fields for NewPerson.
    name: str = Field(min_length=1)  # Declare name and apply the validation constraints or description shown here.
    role: str = Field(min_length=1)  # Declare role and apply the validation constraints or description shown here.
    firm_id: int  # Require the identifier of the firm this person belongs to.


def get_person_or_404(person_id: int) -> dict:  # Find a person by ID or raise an HTTP 404 error.
    for person in PEOPLE:  # Examine each record in the shared in-memory list.
        if person["id"] == person_id:  # Check whether this record has the requested identifier.
            return person  # Return person to the caller.
    raise HTTPException(status_code=404, detail=f"No person with id {person_id}")  # Stop this request and return HTTP 404 with the supplied error detail.


@router.get("")  # Register the following function as the handler for this GET route.
def list_people(firm_id: int | None = None):  # List all people or filter them by firm.
    if firm_id is None:  # Check whether the caller omitted the firm filter.
        return PEOPLE  # Return PEOPLE to the caller.
    return [person for person in PEOPLE if person["firm_id"] == firm_id]  # Return only people associated with the requested firm.

#EOD Wednesday


#get_person

@router.get("/{person_id}")  # Register the following function as the handler for this GET route.
def get_person(person: dict = Depends(get_person_or_404)):  # Return the person resolved by the FastAPI dependency.
    return person  # Return person to the caller.
#Returns the matching person or a 404 if missing. Syntax check passed.

#add_person
@router.post("", status_code=201)  # Register the following function as the handler for this POST route.
def add_person(new: NewPerson):  # Add a person after checking that their firm exists.
    get_firm_or_404(new.firm_id)#raises a 404 if firm doesnt exist
    new_id = max((person["id"] for person in PEOPLE), default=0) + 1  # Choose an identifier one higher than the largest existing identifier.

    person = {  # Build the new person record from the validated request.
        "id": new_id,  # Include the record identifier in this record.
        "name": new.name,  # Include the name in this record.
        "role": new.role,  # Include the message sender role in this record.
        "firm_id": new.firm_id,  # Include the related firm identifier in this record.
    }  # Close the preceding expression or collection.
    PEOPLE.append(person)  # Store the new person in the shared in-memory list.
    return person  # Return person to the caller.
#It checks the firm exists, assigns an ID, saves the person, and returns them.
#Verified successful creation and a 404 for a missing firm.
