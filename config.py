"""
Configuration settings for Ghana Admission Checker
"""
import os

class Config:
    """Base configuration"""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'admission_checker.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-this-in-env-file'
    
    # Extra Security Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600 # 1 hour
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # OCR settings
    USE_OCR = True
    OCR_METHOD = 'easyocr'  # 'easyocr' or 'pytesseract'
    
    # WASSCE grading system
    GRADE_POINTS = {
        'A1': 1, 'B2': 2, 'B3': 3, 'C4': 4, 'C5': 5, 
        'C6': 6, 'D7': 7, 'E8': 8, 'F9': 9
    }
    
    PASSING_GRADES = {'A1', 'B2', 'B3', 'C4', 'C5', 'C6'}
    FAILING_GRADES = {'D7', 'E8', 'F9'}
    
    # Course categories
    COURSE_CATEGORIES = [
        'Science',
        'General Arts',
        'Business',
        'Visual Arts',
        'Home Economics',
        'Technical/Vocational'
    ]
    
    # Core subjects by category
    CORE_SUBJECTS = {
        'Science': ['English Language', 'Core Mathematics', 'Integrated Science'],
        'General Arts': ['English Language', 'Core Mathematics', 'Social Studies'],
        'Business': ['English Language', 'Core Mathematics', 'Social Studies'],
        'Visual Arts': ['English Language', 'Core Mathematics', 'Social Studies'],
        'Home Economics': ['English Language', 'Core Mathematics', 'Social Studies'],
        'Technical/Vocational': ['English Language', 'Core Mathematics', 'Social Studies']
    }
    
    # Common electives
    ELECTIVES = [
        'Additional Mathematics', 'Physics', 'Chemistry', 'Biology',
        'Economics', 'Accounting', 'Business Management', 'Civic Education',
        'History', 'Geography', 'Literature in English', 'French',
        'Clothing and Textiles', 'Food and Nutrition', 'Visual Arts',
        'Music', 'Information and Communication Technology', 'General Knowledge in ICT'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Enforce HTTPS in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Firebase Configuration from Environment (with fallbacks)
def get_firebase_config():
    return {
        "apiKey": os.environ.get('FIREBASE_API_KEY', 'AIzaSyBOmO2zO0qSUhB9CEJ8ynFNwURLvJyiY4A'),
        "authDomain": os.environ.get('FIREBASE_AUTH_DOMAIN', 'studio-2794193502-1482b.firebaseapp.com'),
        "projectId": os.environ.get('FIREBASE_PROJECT_ID', 'studio-2794193502-1482b'),
        "storageBucket": os.environ.get('FIREBASE_STORAGE_BUCKET', 'studio-2794193502-1482b.firebasestorage.app'),
        "messagingSenderId": os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '800219501363'),
        "appId": os.environ.get('FIREBASE_APP_ID', '1:800219501363:web:a5562f6c0af41180112446')
    }
