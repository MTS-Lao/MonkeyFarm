from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .core.config import settings
from .api.endpoints import auth, monkeys, vaccines, users, cases
from .api import deps
from . import crud
from .middleware import AuthMiddleware
from .core import security

from typing import Optional
from sqlalchemy import extract, desc
from app.models import Monkey
from fastapi.responses import StreamingResponse
import csv
import io

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Custom Jinja2 environment with extra functions
templates = Jinja2Templates(directory="app/templates")
templates.env.globals.update({
    'min': min,
    'max': max,
})


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add auth middleware
app.add_middleware(AuthMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(monkeys.router, prefix=f"{settings.API_V1_STR}/monkeys", tags=["monkeys"])
app.include_router(
    vaccines.router,
    prefix=f"{settings.API_V1_STR}/vaccines",
    tags=["vaccines"]
)
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/users",
    tags=["users"]
)
app.include_router(
    cases.router,
    prefix=f"{settings.API_V1_STR}/cases",
    tags=["cases"]
)

@app.get("/")
async def root(request: Request):
    if request.state.user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    user = crud.user.authenticate(
        db, username=username, password=password
    )
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Incorrect username or password"
            },
            status_code=400
        )
    
    access_token = security.create_access_token(subject=user.username)
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        "access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/dashboard")
async def dashboard(
    request: Request,
    db: Session = Depends(deps.get_db)
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    # Redirect staff users away from dashboard
    if not request.state.user.is_admin:
        return RedirectResponse(url="/monkeys")
    
    from .utils.stats import get_dashboard_stats
    dashboard_data = get_dashboard_stats(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": request.state.user,
            **dashboard_data
        }
    )

# Update the root route to redirect staff users to monkeys page
@app.get("/")
async def root(request: Request):
    if request.state.user:
        if request.state.user.is_admin:
            return RedirectResponse(url="/dashboard")
        return RedirectResponse(url="/monkeys")
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.get("/monkeys")
async def list_monkeys(
    request: Request,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    year: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    case_id: Optional[str] = None,
    gender: Optional[str] = None,
    father: Optional[str] = None,
    mother: Optional[str] = None,
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    # Get filter options
    cases = crud.monkey_case.get_multi(db)
    
    # Get unique years from birthday
    years = db.query(extract('year', Monkey.birthday).label('year'))\
        .distinct()\
        .order_by(desc('year'))\
        .all()
    years = [str(year[0]) for year in years]

    # Get unique father and mother codes
    father_codes = db.query(Monkey.father)\
        .filter(Monkey.father.isnot(None))\
        .distinct()\
        .order_by(Monkey.father)\
        .all()
    father_codes = [code[0] for code in father_codes if code[0]]

    mother_codes = db.query(Monkey.mother)\
        .filter(Monkey.mother.isnot(None))\
        .distinct()\
        .order_by(Monkey.mother)\
        .all()
    mother_codes = [code[0] for code in mother_codes if code[0]]
    
    # Handle filters
    filters = {}
    if year and year.strip():
        filters["year"] = year
    if date_from and date_from.strip():
        filters["date_from"] = date_from
    if date_to and date_to.strip():
        filters["date_to"] = date_to
    if case_id and case_id.strip():
        filters["case_id"] = int(case_id)
    if gender and gender.strip():
        filters["gender"] = gender
    if father and father.strip():
        filters["father"] = father
    if mother and mother.strip():
        filters["mother"] = mother
    
    # Pagination
    page_size = 10
    skip = (page - 1) * page_size
    total_count = crud.monkey.get_count(db, filters=filters)
    total_pages = (total_count + page_size - 1) // page_size
    
    monkeys = crud.monkey.get_multi(
        db, 
        skip=skip, 
        limit=page_size,
        filters=filters
    )
    
    return templates.TemplateResponse(
        "monkeys/list.html",
        {
            "request": request,
            "user": request.state.user,
            "monkeys": monkeys,
            "cases": cases,
            "years": years,
            "father_codes": father_codes,
            "mother_codes": mother_codes,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "selected_year": year,
            "selected_date_from": date_from,
            "selected_date_to": date_to,
            "selected_case_id": case_id,
            "selected_gender": gender,
            "selected_father": father,
            "selected_mother": mother
        }
    )

@app.get("/monkeys/create")
async def create_monkey_form(
    request: Request,
    db: Session = Depends(deps.get_db)
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    cases = crud.monkey_case.get_multi(db)
    return templates.TemplateResponse(
        "monkeys/form.html",
        {
            "request": request,
            "user": request.state.user,
            "cases": cases,
            "monkey": None
        }
    )

@app.get("/monkeys/{monkey_id}/edit")
async def edit_monkey_form(
    request: Request,
    monkey_id: int,
    db: Session = Depends(deps.get_db)
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    monkey = crud.monkey.get(db, id=monkey_id)
    if not monkey:
        raise HTTPException(status_code=404, detail="Monkey not found")
    
    cases = crud.monkey_case.get_multi(db)
    return templates.TemplateResponse(
        "monkeys/form.html",
        {
            "request": request,
            "user": request.state.user,
            "monkey": monkey,
            "cases": cases
        }
    )

@app.get("/vaccines")
async def list_vaccines(
    request: Request,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    monkey_id: Optional[str] = None,
    vaccine_id: Optional[str] = None,
    dose: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    # Get all vaccines and monkeys for dropdowns
    vaccines = crud.vaccine.get_multi(db)
    monkeys = crud.monkey.get_multi(db)
    
    # Process filters
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
    
    # Pagination settings
    page_size = 10
    skip = (page - 1) * page_size
    
    # Get total count for pagination
    total_count = crud.vaccination.get_count(db, filters=filters)
    total_pages = (total_count + page_size - 1) // page_size
    
    # Get paginated vaccinations
    vaccinations = crud.vaccination.get_multi(
        db, 
        skip=skip, 
        limit=page_size,
        filters=filters
    )
    
    return templates.TemplateResponse(
        "vaccines/list.html",
        {
            "request": request,
            "user": request.state.user,
            "vaccines": vaccines,
            "monkeys": monkeys,
            "vaccinations": vaccinations,
            "selected_monkey_id": monkey_id,
            "selected_vaccine_id": vaccine_id,
            "selected_dose": dose,
            "selected_date_from": date_from,
            "selected_date_to": date_to,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages
        }
    )

@app.get("/vaccines/export")
async def export_vaccinations(
    request: Request,
    db: Session = Depends(deps.get_db),
    monkey_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    if not request.state.user:
        return RedirectResponse(url="/")
    
    # Get vaccinations with filters
    filters = {}
    if monkey_id:
        filters["monkey_id"] = monkey_id
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    
    vaccinations = crud.vaccination.get_multi(db, skip=0, limit=None, filters=filters)
    
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
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            'Content-Disposition': 'attachment; filename=vaccinations.csv'
        }
    )

@app.get("/settings")
async def settings_page(
    request: Request,
    db: Session = Depends(deps.get_db)
):
    if not request.state.user or not request.state.user.is_admin:
        return RedirectResponse(url="/")
    
    users = crud.user.get_multi(db)
    cases = crud.monkey_case.get_multi(db)
    vaccines = crud.vaccine.get_multi(db)
    
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "user": request.state.user,
            "users": users,
            "cases": cases,
            "vaccines": vaccines
        }
    )

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8372)