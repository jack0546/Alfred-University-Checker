"""
run.py - Quick start script for production
"""
import os
from app import create_app

if __name__ == '__main__':
    config_name = os.getenv('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    +------------------------------------------------------------+
    |   Ghana University Admission Eligibility Checker            |
    |   Starting server...                                        |
    +------------------------------------------------------------+
    
    Configuration: {config_name.upper()}
    Debug Mode: {debug}
    Server: http://{host}:{port}
    
    Press CTRL+C to stop the server
    """)
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )
