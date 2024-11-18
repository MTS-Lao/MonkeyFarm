import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

def reset_admin_password():
    db = SessionLocal()
    try:
        # Find admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Admin user not found")
            return
        
        # Reset password to "admin123"
        new_password = "admin123"
        admin.password = get_password_hash(new_password)
        
        db.commit()
        print(f"Admin password has been reset to: {new_password}")
    
    except Exception as e:
        print(f"Error resetting password: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()