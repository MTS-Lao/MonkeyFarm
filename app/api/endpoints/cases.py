from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ...crud import monkey_case as crud_case
from ...schemas import monkey_case as case_schemas
from ...api import deps

router = APIRouter()

@router.get("/", response_model=List[case_schemas.MonkeyCase])
def get_cases(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve cases.
    """
    return crud_case.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=case_schemas.MonkeyCase)
def create_case(
    db: Session = Depends(deps.get_db),
    name: str = Form(...),
):
    """
    Create new case.
    """
    # Check if case with same name exists
    existing_case = crud_case.get_by_name(db, name=name)
    if existing_case:
        raise HTTPException(
            status_code=400,
            detail="Case with this name already exists"
        )
    
    case_in = case_schemas.MonkeyCaseCreate(name=name)
    return crud_case.create(db, obj_in=case_in)

@router.get("/{case_id}", response_model=case_schemas.MonkeyCase)
def get_case(
    case_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get case by ID.
    """
    case = crud_case.get(db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=case_schemas.MonkeyCase)
def update_case(
    case_id: int,
    name: str = Form(...),
    db: Session = Depends(deps.get_db),
):
    """
    Update case.
    """
    case = crud_case.get(db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check if name is taken by another case
    existing_case = crud_case.get_by_name(db, name=name)
    if existing_case and existing_case.id != case_id:
        raise HTTPException(
            status_code=400,
            detail="Case with this name already exists"
        )
    
    case_in = case_schemas.MonkeyCaseUpdate(name=name)
    return crud_case.update(db, db_obj=case, obj_in=case_in)

@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Delete case.
    """
    case = crud_case.get(db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check if case is being used by any monkeys
    if len(case.monkeys) > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete case that is being used by monkeys"
        )
    
    crud_case.remove(db, id=case_id)
    return {"status": "success"}