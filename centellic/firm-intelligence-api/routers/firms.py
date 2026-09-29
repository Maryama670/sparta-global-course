from fastapi import APIRouter, Depends, Header, HTTPException  # Import route grouping, dependency injection, header reading and HTTP error helpers.
from pydantic import BaseModel, Field  # Import BaseModel for validated data schemas and Field for field constraints and descriptions.

from data import FIRMS  # Import the shared in-memory list of firm records.


router = APIRouter(prefix="/firms", tags=["firms"])  # Group these endpoints under the configured URL prefix and documentation tag.
_seen_keys:dict[str, dict] = {}  # Remember created firms by idempotency key to avoid duplicate creation.


class NewFirm(BaseModel):  # Define the validated fields for NewFirm.
    # name, jurisdiction, revenue, lawyers, equity_partners
    name: str = Field(min_length=1)  # Declare name and apply the validation constraints or description shown here.
    jurisdiction: str = Field(min_length=2, max_length=5)  # Declare jurisdiction and apply the validation constraints or description shown here.
    revenue_usd_m: float = Field(gt=0)  # Declare revenue_usd_m and apply the validation constraints or description shown here.
    lawyers: int = Field(gt=0)  # Declare lawyers and apply the validation constraints or description shown here.
    equity_partners: int = Field(gt=0)  # Declare equity_partners and apply the validation constraints or description shown here.


def get_firm_or_404(firm_id: int) -> dict:  # Find a firm by ID or raise an HTTP 404 error.
    for firm in FIRMS:  # Examine each record in the shared in-memory list.
        if firm["id"] == firm_id:  # Check whether this record has the requested identifier.
            return firm  # Return firm to the caller.
    raise HTTPException(status_code=404, detail=f"No firm with id {firm_id}")  # Stop this request and return HTTP 404 with the supplied error detail.


@router.get("")  # Register the following function as the handler for this GET route.
def list_firms(jurisdiction: str | None = None, min_revenue: float | None = None):  # List firms with optional jurisdiction and revenue filters.
    results = FIRMS  # Start with all firms before applying optional filters.
    if jurisdiction is not None:  # Apply a jurisdiction filter only when one was supplied.
        results = [f for f in results if f["jurisdiction"] == jurisdiction]  # Keep firms whose jurisdiction matches the requested value.
    if min_revenue is not None:  # Apply a minimum revenue filter only when one was supplied.
        results = [f for f in results if f["revenue_usd_m"] >= min_revenue]  # Keep firms at or above the requested revenue in millions of dollars.
    return results  # Return results to the caller.


@router.get("/{firm_id}")  # Register the following function as the handler for this GET route.
def get_firm(firm: dict = Depends(get_firm_or_404)):  # Return the firm resolved by the FastAPI dependency.
    return firm  # Return firm to the caller.


# Revenue per lawyer uses total revenue divided by lawyer headcount.
# Profit per equity partner assumes a 35% profit margin.
@router.get("/{firm_id}/benchmarks")  # Register the following function as the handler for this GET route.
def get_benchmarks(firm: dict = Depends(get_firm_or_404)):  # Calculate revenue per lawyer and estimated profit per equity partner.
    revenue = firm["revenue_usd_m"]  # Read the firm revenue, measured in millions of US dollars.
    return {  # Build and return a dictionary containing the following fields.
        "id": firm["id"],  # Include the record identifier in this record.
        "name": firm["name"],  # Include the name in this record.
        "revenue_per_lawyer_usd": round(  # Round revenue per lawyer to the nearest whole dollar.
            revenue * 1_000_000 / firm["lawyers"]  # Convert revenue to dollars and divide by lawyer headcount.
        ),  # Close the preceding expression or collection.
        "profit_per_equity_partner": round(  # Round estimated profit per equity partner to the nearest whole dollar.
            revenue * 1_000_000 * 0.35 / firm["equity_partners"]  # Estimate profit at a 35 percent margin and divide by equity partners.
        ),  # Close the preceding expression or collection.
    }  # Close the preceding expression or collection.
#post
# /firms

@router.post("", status_code=201)  # Register the following function as the handler for this POST route.
def add_firm(new: NewFirm, idempotency_key: str | None = Header(default=None)):  # Create a firm, reusing a prior result for a repeated idempotency key.
    if idempotency_key is not None and idempotency_key in _seen_keys:  # Check whether this creation request has already been handled.
        return _seen_keys[idempotency_key]  # Return the previously created firm for this request key.

    new_id = max((firm["id"] for firm in FIRMS), default=0) + 1  # Choose an identifier one higher than the largest existing identifier.
    firm = {  # Build the new firm record from the validated request.
        "id": new_id,  # Include the record identifier in this record.
        "name": new.name,  # Include the name in this record.
        "jurisdiction": new.jurisdiction,  # Include the jurisdiction in this record.
        "revenue_usd_m": new.revenue_usd_m,  # Include revenue in millions of US dollars in this record.
        "lawyers": new.lawyers,  # Include the lawyer headcount in this record.
        "equity_partners": new.equity_partners,  # Include the equity partner count in this record.
    }  # Close the preceding expression or collection.
    FIRMS.append(firm)  # Store the new firm in the shared in-memory list.
    if idempotency_key is not None:  # Cache the result only when the caller supplied an idempotency key.
        _seen_keys[idempotency_key] = firm  # Associate this request key with the firm just created.
    return firm  # Return firm to the caller.


@router.put("/{firm_id}")  # Register the following function as the handler for this PUT route.
def update_firm(new: NewFirm, firm: dict = Depends(get_firm_or_404)):  # Replace the editable fields of an existing firm.
    firm["name"] = new.name  # Replace this stored firm field with the validated incoming value.
    firm["jurisdiction"] = new.jurisdiction  # Replace this stored firm field with the validated incoming value.
    firm["revenue_usd_m"] = new.revenue_usd_m  # Replace this stored firm field with the validated incoming value.
    firm["lawyers"] = new.lawyers  # Replace this stored firm field with the validated incoming value.
    firm["equity_partners"] = new.equity_partners  # Replace this stored firm field with the validated incoming value.

    return firm  # Return firm to the caller.


@router.delete("/{firm_id}", status_code=204)  # Register the following function as the handler for this DELETE route.
def delete_firm(firm: dict = Depends(get_firm_or_404)):  # Delete an existing firm.
    FIRMS.remove(firm)  # Remove the matching firm from the shared in-memory list.
    return  # Finish the handler without returning a response body.

