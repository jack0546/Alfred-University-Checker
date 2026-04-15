"""
Database models for Ghana Admission Checker
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from json import dumps, loads

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Null if Google/Firebase login only
    name = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)
    profile_pic = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

class Student(db.Model):
    """Student model to store student submission data"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # Science, Arts, etc.
    
    # Result data
    core_subjects = db.Column(db.JSON, nullable=False)  # JSON object with subject: grade
    electives = db.Column(db.JSON, nullable=False)  # JSON object with subject: grade
    
    # Aggregate calculation
    aggregate = db.Column(db.Integer, nullable=True)
    core_aggregate = db.Column(db.Integer, nullable=True)
    electives_aggregate = db.Column(db.Integer, nullable=True)
    
    # Status
    verified = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    payment_reference = db.Column(db.String(100), nullable=True)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Result slip info
    result_slip_path = db.Column(db.String(500), nullable=True)
    ocr_used = db.Column(db.Boolean, default=False)
    
    # Admission results
    qualified_programs = db.Column(db.JSON, nullable=True)  # List of qualified programs
    borderline_programs = db.Column(db.JSON, nullable=True)  # List of borderline programs
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'category': self.category,
            'core_subjects': self.core_subjects,
            'electives': self.electives,
            'aggregate': self.aggregate,
            'verified': self.verified,
            'is_paid': self.is_paid,
            'submission_date': self.submission_date.isoformat()
        }

class University(db.Model):
    """University model"""
    __tablename__ = 'universities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    abbreviation = db.Column(db.String(20), nullable=True)
    type = db.Column(db.String(50), nullable=False)  # 'Traditional' or 'Technical'
    city = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    programs = db.relationship('Program', backref='university', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'type': self.type,
            'city': self.city,
            'website': self.website,
            'description': self.description,
            'program_count': len(self.programs)
        }

class Program(db.Model):
    """Program/Course model"""
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)  # e.g., Engineering, Science, Business
    description = db.Column(db.Text, nullable=True)
    
    # Admission requirements
    maximum_aggregate = db.Column(db.Integer, nullable=False)  # Lower is better in Ghana system
    minimum_aggregate = db.Column(db.Integer, nullable=True)
    required_core_subjects = db.Column(db.JSON, nullable=False)  # List of required subjects
    required_electives = db.Column(db.JSON, nullable=True)  # List of preferred/required electives
    
    # Additional requirements
    minimum_credit_passes = db.Column(db.Integer, default=3)  # Typically 3 credits in core subjects
    course_categories = db.Column(db.JSON, nullable=True)  # Allowed course categories
    
    # Academic year tracking
    academic_year = db.Column(db.Integer, default=lambda: datetime.utcnow().year)  # Year of cutoff validity
    
    # Program popularity and value categorization
    popularity_level = db.Column(db.String(20), default='medium')  # 'high', 'medium', 'low' (how popular)
    value_level = db.Column(db.String(20), default='medium')  # 'high', 'medium', 'low' (how valuable/competitive)
    is_desired_program = db.Column(db.Boolean, default=False)  # Flag for highly desired programs
    
    # Metadata
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            'university_name': self.university.name,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'maximum_aggregate': self.maximum_aggregate,
            'minimum_aggregate': self.minimum_aggregate,
            'required_core_subjects': self.required_core_subjects,
            'required_electives': self.required_electives,
            'minimum_credit_passes': self.minimum_credit_passes,
            'academic_year': self.academic_year,
            'last_updated': self.last_updated.isoformat()
        }

class CutoffPoint(db.Model):
    """Track cutoff point changes per program and academic year"""
    __tablename__ = 'cutoff_points'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    academic_year = db.Column(db.Integer, nullable=False)  # e.g., 2026
    
    # Cutoff data
    maximum_aggregate = db.Column(db.Integer, nullable=False)
    minimum_aggregate = db.Column(db.Integer, nullable=True)
    
    # Metadata
    updated_by = db.Column(db.String(255), nullable=True)  # Admin who updated
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)  # Reason for change
    is_official = db.Column(db.Boolean, default=False)  # Official vs provisional
    
    # For audit trail
    previous_maximum_aggregate = db.Column(db.Integer, nullable=True)
    change_reason = db.Column(db.String(500), nullable=True)
    
    program = db.relationship('Program', backref='cutoff_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'academic_year': self.academic_year,
            'maximum_aggregate': self.maximum_aggregate,
            'minimum_aggregate': self.minimum_aggregate,
            'previous_maximum_aggregate': self.previous_maximum_aggregate,
            'change_reason': self.change_reason,
            'updated_by': self.updated_by,
            'update_date': self.update_date.isoformat(),
            'is_official': self.is_official
        }

class AdmissionResult(db.Model):
    """Admission check result"""
    __tablename__ = 'admission_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    
    status = db.Column(db.String(20), nullable=False)  # 'qualified', 'borderline', 'not_qualified'
    reason = db.Column(db.Text, nullable=True)
    
    matched_subjects = db.Column(db.JSON, nullable=True)
    missing_subjects = db.Column(db.JSON, nullable=True)
    
    check_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='admission_results')
    program = db.relationship('Program')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'program_id': self.program_id,
            'program_name': self.program.name,
            'university_name': self.program.university.name,
            'status': self.status,
            'reason': self.reason,
            'matched_subjects': self.matched_subjects,
            'missing_subjects': self.missing_subjects,
            'check_date': self.check_date.isoformat()
        }
