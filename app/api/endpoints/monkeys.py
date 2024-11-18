from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form
from sqlalchemy.orm import Session
from datetime import date, datetime
from ...crud import monkey as crud_monkey
from ...schemas import monkey as monkey_schemas
from ...api import deps
from ...models import Monkey, Gender

router = APIRouter()

@router.get("/", response_model=List[monkey_schemas.Monkey])
def get_monkeys(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    year: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    case_id: Optional[int] = None,
    gender: Optional[str] = None,
    father: Optional[str] = None,
    mother: Optional[str] = None,
):
    """
    Retrieve monkeys with filters.
    """
    filters = {}
    
    if year and year.strip():
        filters["year"] = year
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    if case_id:
        filters["case_id"] = case_id
    if gender and gender.strip():
        filters["gender"] = gender
    if father and father.strip():
        filters["father"] = father
    if mother and mother.strip():
        filters["mother"] = mother
    
    return crud_monkey.get_multi(db, skip=skip, limit=limit, filters=filters)

@router.post("/", response_model=monkey_schemas.Monkey)
async def create_monkey(
    code: str = Form(...),
    case_id: int = Form(...),
    birthday: date = Form(...),
    gender: Gender = Form(...),
    father: Optional[str] = Form(None),
    mother: Optional[str] = Form(None),
    special_characteristics: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db),
):
    """
    Create new monkey.
    """
    # Convert form data to MonkeyCreate schema
    monkey_data = {
        "code": code,
        "case_id": case_id,
        "birthday": birthday,
        "gender": gender,
        "father": father,
        "mother": mother,
        "special_characteristics": special_characteristics
    }
    monkey_in = monkey_schemas.MonkeyCreate(**monkey_data)

    # Check if monkey code already exists
    existing_monkey = crud_monkey.get_by_code(db, code=monkey_in.code)
    if existing_monkey:
        raise HTTPException(
            status_code=400,
            detail="A monkey with this code already exists."
        )
    
    return crud_monkey.create(db, obj_in=monkey_in)

@router.get("/{monkey_id}", response_model=monkey_schemas.Monkey)
def get_monkey(
    monkey_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get monkey by ID.
    """
    monkey = crud_monkey.get(db, id=monkey_id)
    if not monkey:
        raise HTTPException(status_code=404, detail="Monkey not found")
    return monkey

@router.put("/{monkey_id}", response_model=monkey_schemas.Monkey)
async def update_monkey(
    monkey_id: int,
    code: str = Form(...),
    case_id: int = Form(...),
    birthday: date = Form(...),
    gender: Gender = Form(...),
    father: Optional[str] = Form(None),
    mother: Optional[str] = Form(None),
    special_characteristics: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db),
):
    """
    Update monkey.
    """
    monkey = crud_monkey.get(db, id=monkey_id)
    if not monkey:
        raise HTTPException(status_code=404, detail="Monkey not found")

    # Convert form data to update schema
    update_data = {
        "code": code,
        "case_id": case_id,
        "birthday": birthday,
        "gender": gender,
        "father": father,
        "mother": mother,
        "special_characteristics": special_characteristics
    }
    
    # Check for existing code if code is being changed
    if update_data["code"] != monkey.code:
        existing_monkey = crud_monkey.get_by_code(db, code=update_data["code"])
        if existing_monkey:
            raise HTTPException(
                status_code=400,
                detail="A monkey with this code already exists."
            )

    return crud_monkey.update(db, db_obj=monkey, obj_in=update_data)

@router.delete("/{monkey_id}")
def delete_monkey(
    monkey_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Delete monkey.
    """
    monkey = crud_monkey.get(db, id=monkey_id)
    if not monkey:
        raise HTTPException(status_code=404, detail="Monkey not found")
    crud_monkey.remove(db, id=monkey_id)
    return {"status": "success"}