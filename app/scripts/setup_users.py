import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

def setup_users():
    db = SessionLocal()
    try:
        # Clear existing users
        db.query(User).delete()
        
        # Create admin user
        admin = User(
            username="admin",
            password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin)
        
        # Create test staff user
        staff = User(
            username="staff",
            password=get_password_hash("staff123"),
            is_admin=False
        )
        db.add(staff)
        
        db.commit()
        print("Successfully created admin and staff users:")
        print("Admin - username: admin, password: admin123")
        print("Staff - username: staff, password: staff123")
    
    except Exception as e:
        print(f"Error setting up users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_users()