from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.user import User
from app.enums.role import UserRole
from app.core.security import hash_password


def seed_admin():
    db: Session = SessionLocal()

    try:
        # If any user exists, do nothing
        if db.query(User).count() > 0:
            print("Users already exist. Skipping admin seed.")
            return

        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("Admin@123"),
            role=UserRole.ADMIN.value,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("✅ Default admin created.")

    except Exception as e:
        print(f"❌ Admin seed failed: {e}")
        db.rollback()

    finally:
        db.close()