import asyncio
from app.database import SessionLocal
from app.models import Base
from app.core.security import get_password_hash
from app.models import User
from app import crud

async def init_db():
    db = SessionLocal()
    try:
        # Create initial admin user
        admin_user = crud.user.get_by_username(db, username="admin")
        if not admin_user:
            user_in = {
                "username": "admin",
                "password": get_password_hash("admin123"),
                "is_admin": True
            }
            crud.user.create(db, obj_in=user_in)
            print("Created admin user")

        # Create initial cases
        initial_cases = ["A-01", "A-02", "B-01", "B-02"]
        for case_name in initial_cases:
            existing_case = crud.monkey_case.get_by_name(db, name=case_name)
            if not existing_case:
                case_in = {"name": case_name}
                crud.monkey_case.create(db, obj_in=case_in)
                print(f"Created case: {case_name}")

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(init_db())