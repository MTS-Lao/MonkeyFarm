import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

def create_first_user():
    db = SessionLocal()
    
    # Check if admin user already exists
    if db.query(User).filter(User.username == "admin").first():
        print("Admin user already exists")
        return
    
    # Create admin user
    admin_user = User(
        username="admin",
        password=get_password_hash("admin123"),  # Change this password!
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    print("Admin user created successfully")

if __name__ == "__main__":
    create_first_user()