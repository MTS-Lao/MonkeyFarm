import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import Monkey, MonkeyCase

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%b-%y').date()
    except ValueError:
        print(f"Error parsing date: {date_str}")
        return None

def import_initial_data():
    db = SessionLocal()
    
    # First, check if we already have data
    if db.query(Monkey).count() > 0:
        print("Data already exists in the database. Skipping import.")
        return

    # Create required cases first
    cases_data = [
        {"name": "A-01"}  # All monkeys are in A-01 from the sample data
    ]

    cases = {}
    for case_data in cases_data:
        case = MonkeyCase(**case_data)
        db.add(case)
        db.flush()  # This will assign the ID
        cases[case.name] = case.id

    # Data from your CSV
    monkeys_data = [
        {"code": "A242/19", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S198/20", "date_of_birth": "12-Jul-21"},
        {"code": "C319F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S024/21", "date_of_birth": "31-Jan-22"},
        {"code": "E027/19", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S042/20", "date_of_birth": "3-Sep-21"},
        {"code": "E266F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S010/20", "date_of_birth": "14-Aug-21"},
        {"code": "E264F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S300/21", "date_of_birth": "12-Jul-21"},
        {"code": "C247F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S001/21", "date_of_birth": "3-Sep-21"},
        {"code": "AM015/21", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S009/20", "date_of_birth": "3-Sep-21"},
        {"code": "J902", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S100/21", "date_of_birth": "12-Jul-21"},
        {"code": "J906", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S089/20", "date_of_birth": "14-Aug-21"},
        {"code": "C280F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S097/19", "date_of_birth": "12-Jul-21"},
        {"code": "C263F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S173/20", "date_of_birth": "12-Jul-21"},
        {"code": "C324F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S006/20", "date_of_birth": "14-Aug-21"},
        {"code": "J919", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S112/20", "date_of_birth": "31-Jan-22"},
        {"code": "J917", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S044/20", "date_of_birth": "29-Jan-22"},
        {"code": "AM008/21", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S032/20", "date_of_birth": "31-Jan-22"},
        {"code": "C321F", "house_number": "A-01", "gender": "M", "father": "DC081", "mother": "S054/20", "date_of_birth": "30-Jan-22"},
        {"code": "C252F", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S086/19", "date_of_birth": "31-Jan-22"},
        {"code": "AM007/21", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S148/21", "date_of_birth": "30-Jan-22"},
        {"code": "J904", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S076/21", "date_of_birth": "31-Jan-22"},
        {"code": "AM020/19", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S283/21", "date_of_birth": "14-Aug-21"},
        {"code": "C138/19", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S195/21", "date_of_birth": "28-Jan-22"},
        {"code": "C322F", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S308/21", "date_of_birth": "14-Aug-21"},
        {"code": "C294F", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S010/19", "date_of_birth": "28-Jan-22"},
        {"code": "NNF039", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S148/21", "date_of_birth": "28-Jan-22"},
        {"code": "EC087/19", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S143/21", "date_of_birth": "28-Jan-22"},
        {"code": "A09", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S167/21", "date_of_birth": "5-Sep-21"},
        {"code": "A1268", "house_number": "A-01", "gender": "M", "father": "D5001", "mother": "S059/21", "date_of_birth": "28-Jan-22"},
        {"code": "A1284", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S220/21", "date_of_birth": "28-Jan-22"},
        {"code": "S3576", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S224/21", "date_of_birth": "28-Jan-22"},
        {"code": "F4M092", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S075/21", "date_of_birth": "14-Jul-21"},
        {"code": "A2140", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S264/21", "date_of_birth": "20-Sep-21"},
        {"code": "E16", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S127/21", "date_of_birth": "21-Sep-21"},
        {"code": "FD186/19", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S155/21", "date_of_birth": "20-Jan-22"},
        {"code": "A6487", "house_number": "A-01", "gender": "M", "father": "D5002", "mother": "S315/21", "date_of_birth": "26-Jan-22"},
        {"code": "A10", "house_number": "A-01", "gender": "M", "father": "D5060", "mother": "C001F", "date_of_birth": "31-Jan-22"}
    ]

    # Import monkey data
    try:
        for data in monkeys_data:
            monkey = Monkey(
                code=data["code"],
                case_id=cases[data["house_number"]],
                birthday=parse_date(data["date_of_birth"]),
                gender=data["gender"],
                father=data["father"],
                mother=data["mother"]
            )
            db.add(monkey)
        
        db.commit()
        print("Successfully imported initial data")
    
    except Exception as e:
        print(f"Error importing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_initial_data()