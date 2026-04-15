"""
Database initialization and utilities
"""
from models import db, University, Program
import json
import os
from config import Config

def init_database(app):
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        # Load initial data if database is empty
        if University.query.count() == 0:
            load_universities_data()

def load_universities_data():
    """Load universities and programs from JSON data"""
    data_file = os.path.join(Config.BASE_DIR, 'data', 'universities_data.json')
    
    if not os.path.exists(data_file):
        print(f"Warning: {data_file} not found. Skipping initial data load.")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add universities and programs
    for uni_data in data['universities']:
        # Check if university already exists
        university = University.query.filter_by(name=uni_data['name']).first()
        if not university:
            university = University(
                name=uni_data['name'],
                abbreviation=uni_data.get('abbreviation'),
                type=uni_data['type'],
                city=uni_data.get('city'),
                website=uni_data.get('website'),
                description=uni_data.get('description')
            )
            db.session.add(university)
            db.session.flush()
        
        # Add programs for this university
        for prog_data in uni_data.get('programs', []):
            program = Program.query.filter_by(
                university_id=university.id,
                name=prog_data['name']
            ).first()
            
            if not program:
                program = Program(
                    university_id=university.id,
                    name=prog_data['name'],
                    category=prog_data.get('category'),
                    description=prog_data.get('description'),
                    maximum_aggregate=prog_data.get('maximum_aggregate', 30),
                    minimum_aggregate=prog_data.get('minimum_aggregate', 6),
                    required_core_subjects=prog_data.get('required_core_subjects', []),
                    required_electives=prog_data.get('required_electives'),
                    course_categories=prog_data.get('course_categories', []),
                    academic_year=prog_data.get('academic_year', 2026),
                    popularity_level=prog_data.get('popularity_level', 'medium'),
                    value_level=prog_data.get('value_level', 'medium'),
                    is_desired_program=prog_data.get('is_desired_program', False),
                    minimum_credit_passes=prog_data.get('minimum_credit_passes', 3)
                )
                db.session.add(program)
    
    db.session.commit()
    print("Database initialized with universities and programs.")

def clear_database():
    """Clear all data from database"""
    db.drop_all()
    db.create_all()
