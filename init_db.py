from models.base import get_engine, init_db, get_session
from models.user import User
from models.contact import Contact
from models.task import Task

def create_admin_user(session):
    # Check if admin user already exists
    admin = session.query(User).filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin')  # Default password
        session.add(admin)
        session.commit()
        print("Created admin user (username: admin, password: admin)")
    else:
        print("Admin user already exists")

def init_database():
    # Create engine and initialize database
    engine = get_engine()
    init_db(engine)
    
    # Create session and admin user
    session = get_session(engine)
    create_admin_user(session)
    session.close()

if __name__ == '__main__':
    init_database()
