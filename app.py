"""
Ghana University Admission Eligibility Checker
Main Application Entry Point
"""
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from config import Config, config, get_firebase_config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_name=os.getenv('FLASK_CONFIG', 'development')):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS (Restricted to trusted origins in production)
    if app.config['DEBUG']:
        CORS(app)
    else:
        # Add your Render domain(s) here
        render_domains = os.environ.get('ALLOWED_ORIGINS', 'https://alfredakwetey.me').split(',')
        CORS(app, resources={r"/api/*": {"origins": render_domains}})

    # Security Headers (Talisman)
    csp = {
        'default-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
            'https://www.gstatic.com',
            'https://*.googleapis.com',
            'https://fonts.gstatic.com',
            'https://*.paystack.co',
            'https://paystack.com',
            'data:'
        ],
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://cdn.jsdelivr.net',
            'https://www.gstatic.com',
            'https://js.paystack.co'
        ],
        'connect-src': [
            '\'self\'',
            'https://*.paystack.co',
            'https://paystack.com',
            'https://*.googleapis.com',
            'https://www.gstatic.com',
            'https://identitytoolkit.googleapis.com',
            'https://securetoken.googleapis.com',
            'https://firebase.googleapis.com',
            'https://*.firebase.com'
        ],
        'frame-src': [
            '\'self\'',
            'https://js.paystack.co',
            'https://standard.paystack.co',
            'https://checkout.paystack.co',
            'https://accounts.google.com',
            'https://*.firebase.com'
        ],
        'frame-src': [
            '\'self\'',
            'https://js.paystack.co',
            'https://standard.paystack.co',
            'https://checkout.paystack.com',
            'https://accounts.google.com'
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com',
            'https://cdnjs.cloudflare.com'
        ]
    }
    Talisman(app, content_security_policy=csp, force_https=(not app.config['DEBUG']))

    # CSRF Protection
    csrf = CSRFProtect(app)
    
    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Create upload folder
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize database
    from models import db
    db.init_app(app)
    
    # Initialize database with data
    from database import init_database, load_universities_data
    init_database(app)
    
    # Register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)

    # Context Processor for Firebase Config
    @app.context_processor
    def inject_firebase():
        return dict(firebase_config=get_firebase_config())
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', 
                              error_code=404, 
                              error_message='Page not found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html',
                              error_code=500,
                              error_message='Internal server error'), 500
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
