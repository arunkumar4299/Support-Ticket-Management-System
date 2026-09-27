from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password


def seed_users():
    db: Session = SessionLocal()

    try:
        # Create Admin
        admin = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()

        if not admin:
            admin = User(
                name="System Admin",
                email="admin@example.com",
                password_hash=hash_password("Admin@123"),
                role=UserRole.ADMIN,
            )

            db.add(admin)
            print("Admin user created.")
        else:
            print("Admin already exists.")

        # Create Support Agent
        agent = db.query(User).filter(
            User.email == "agent@example.com"
        ).first()

        if not agent:
            agent = User(
                name="Support Agent",
                email="agent@example.com",
                password_hash=hash_password("Agent@123"),
                role=UserRole.SUPPORT_AGENT,
            )

            db.add(agent)
            print("Support Agent created.")
        else:
            print("Support Agent already exists.")

        db.commit()
        print("Seed completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()