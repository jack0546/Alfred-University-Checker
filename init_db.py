from app import create_app
from models import db
from database import load_universities_data

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    load_universities_data()
    print('Database initialized successfully with new schema and program descriptions.')
