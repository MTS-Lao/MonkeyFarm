# app/api/endpoints/vaccines.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import date

from ...crud import vaccine as crud_vaccine
from ...crud import vaccination as crud_vaccination
from ...schemas import vaccine as vaccine_schemas
from ...schemas import vaccination as vaccination_schemas
from ...api import deps
from fastapi.responses import StreamingResponse
from datetime import datetime
import csv
import io

router = APIRouter()

# Simplified API routes without response models initially
@router.get("/")
def get_vaccines(db: Session = Depends(deps.get_db)):
    return [vaccine.__dict__ for vaccine in crud_vaccine.get_multi(db)]

@router.post("/")
def create_vaccine(
    db: Session = Depends(deps.get_db),
    name: str = Form(...),
    description: str = Form(None)
):
    vaccine_in = vaccine_schemas.VaccineCreate(name=name, description=description)
    return crud_vaccine.create(db, obj_in=vaccine_in)

@router.put("/{vaccine_id}")
def update_vaccine(
    vaccine_id: int,
    db: Session = Depends(deps.get_db),
    name: str = Form(...),
    description: str = Form(None)
):
    vaccine = crud_vaccine.get(db, id=vaccine_id)
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    
    vaccine_in = vaccine_schemas.VaccineUpdate(name=name, description=description)
    return crud_vaccine.update(db, db_obj=vaccine, obj_in=vaccine_in)

@router.delete("/{vaccine_id}")
def delete_vaccine(
    vaccine_id: int,
    db: Session = Depends(deps.get_db)
):
    vaccine = crud_vaccine.get(db, id=vaccine_id)
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    crud_vaccine.remove(db, id=vaccine_id)
    return {"status": "success"}

@router.get("/vaccinations")
def get_vaccinations(
    db: Session = Depends(deps.get_db),
    page: int = 1,  # Add pagination parameters
    page_size: int = 10,  # Default page size
    monkey_id: Optional[int] = None,
    vaccine_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    dose: Optional[int] = None
):
    filters = {}
    if monkey_id:
        filters["monkey_id"] = monkey_id
    if vaccine_id:
        filters["vaccine_id"] = vaccine_id
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    if dose:
        filters["dose"] = dose

    # Calculate skip for pagination
    skip = (page - 1) * page_size
    
    # Get total count for pagination
    total_count = crud_vaccination.get_count(db, filters=filters)
    total_pages = (total_count + page_size - 1) // page_size
    
    # Get paginated results
    vaccinations = crud_vaccination.get_multi(
        db, 
        skip=skip, 
        limit=page_size,
        filters=filters
    )
    
    return {
        "items": vaccinations,
        "total_count": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "has_next": page < total_pages
    }

@router.post("/vaccinations")
def create_vaccination(
    db: Session = Depends(deps.get_db),
    monkey_id: int = Form(...),
    vaccine_id: int = Form(...),
    date: date = Form(...),
    dose: int = Form(...)
):
    vaccination_in = vaccination_schemas.VaccinationCreate(
        monkey_id=monkey_id,
        vaccine_id=vaccine_id,
        date=date,
        dose=dose
    )
    return crud_vaccination.create(db, obj_in=vaccination_in)

@router.put("/vaccinations/{vaccination_id}")
def update_vaccination(
    vaccination_id: int,
    db: Session = Depends(deps.get_db),
    monkey_id: int = Form(...),
    vaccine_id: int = Form(...),
    date: date = Form(...),
    dose: int = Form(...)
):
    vaccination = crud_vaccination.get(db, id=vaccination_id)
    if not vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    vaccination_in = vaccination_schemas.VaccinationUpdate(
        monkey_id=monkey_id,
        vaccine_id=vaccine_id,
        date=date,
        dose=dose
    )
    return crud_vaccination.update(db, db_obj=vaccination, obj_in=vaccination_in)

@router.get("/vaccinations/{vaccination_id}")
def get_vaccination(
    vaccination_id: int,
    db: Session = Depends(deps.get_db)
):
    vaccination = crud_vaccination.get(db, id=vaccination_id)
    if not vaccination:
        raise HTTPException(status_code=404, detail="Vaccination record not found")
    return {
        "id": vaccination.id,
        "monkey_id": vaccination.monkey_id,
        "vaccine_id": vaccination.vaccine_id,
        "date": vaccination.date.isoformat(),
        "dose": vaccination.dose
    }

@router.get("/export-vaccinations")  # Changed route path
def export_vaccinations(
    db: Session = Depends(deps.get_db),
    monkey_id: Optional[str] = None,
    vaccine_id: Optional[str] = None,
    dose: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    # Process filters - handle empty strings
    filters = {}
    if monkey_id and monkey_id.strip():
        filters["monkey_id"] = int(monkey_id)
    if vaccine_id and vaccine_id.strip():
        filters["vaccine_id"] = int(vaccine_id)
    if dose and dose.strip():
        filters["dose"] = int(dose)
    if date_from and date_from.strip():
        filters["date_from"] = date_from
    if date_to and date_to.strip():
        filters["date_to"] = date_to
        
    vaccinations = crud_vaccination.get_multi(db, filters=filters)
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Date', 'Monkey Code', 'Vaccine Name', 'Dose'])
    
    # Write data
    for vaccination in vaccinations:
        writer.writerow([
            vaccination.date.strftime('%Y-%m-%d'),
            vaccination.monkey.code,
            vaccination.vaccine.name,
            vaccination.dose
        ])
    
    output.seek(0)
    
    # Set filename with timestamp
    filename = f'vaccinations_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )