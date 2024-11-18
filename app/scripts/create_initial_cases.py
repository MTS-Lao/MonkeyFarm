import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import MonkeyCase

def create_initial_cases():
    db = SessionLocal()
    
    # Check if cases already exist
    existing_cases = db.query(MonkeyCase).count()
    if existing_cases > 0:
        print("Cases already exist in database")
        return

    # Create cases from your sample data
    cases = [
        MonkeyCase(name="A-01"),
        MonkeyCase(name="A-02"),
        MonkeyCase(name="B-01"),
        MonkeyCase(name="B-02"),
        MonkeyCase(name="C-01"),
        MonkeyCase(name="C-02"),
    ]
    
    try:
        db.bulk_save_objects(cases)
        db.commit()
        print("Successfully created initial cases")
    except Exception as e:
        print(f"Error creating cases: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_cases()