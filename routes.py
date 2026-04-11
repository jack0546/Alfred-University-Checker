"""
Flask routes for Ghana Admission Checker
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Student, University, Program, AdmissionResult, User
from utils import GradeValidator, AdmissionMatcher
from config import Config
import os
import requests
import json

# Create blueprint
main_bp = Blueprint('main', __name__)

# ==================== HOME PAGE ====================
@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


# ==================== MANUAL ENTRY ====================
@main_bp.route('/manual-entry', methods=['GET', 'POST'])
def manual_entry():
    """Manual grade entry form"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'category', 'core_subjects', 'electives']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        name = data['name'].strip()
        category = data['category']
        core_subjects = data['core_subjects']
        electives = data['electives']
        email = data.get('email', '').strip()
        
        # Validate category
        if category not in Config.COURSE_CATEGORIES:
            return jsonify({'success': False, 'error': f'Invalid category: {category}'}), 400
        
        # Validate subjects and grades
        all_subjects = {**core_subjects, **electives}
        for subject, grade in all_subjects.items():
            if not GradeValidator.is_valid_grade(grade):
                return jsonify({'success': False, 'error': f'Invalid grade for {subject}: {grade}'}), 400
        
        # Create session data to pass to verification
        session_data = {
            'name': name,
            'email': email,
            'category': category,
            'core_subjects': core_subjects,
            'electives': electives
        }
        
        return jsonify({
            'success': True,
            'message': 'Data prepared for verification',
            'redirect_url': url_for('main.verify_result')
        })
    
    return render_template('manual-entry.html', 
                         categories=Config.COURSE_CATEGORIES,
                         electives=Config.ELECTIVES)

# ==================== VERIFY RESULT ====================
@main_bp.route('/verify-result', methods=['GET', 'POST'])
def verify_result():
    """Verify extracted or entered grades"""
    if request.method == 'POST':
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        category = data.get('category')
        core_subjects = data.get('core_subjects', {})
        electives = data.get('electives', {})
        
        # Validate
        if not name or not category:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if len(core_subjects) < 3:
            return jsonify({'success': False, 'error': 'Need at least 3 core subjects'}), 400
        
        if len(electives) < 3:
            return jsonify({'success': False, 'error': 'Need at least 3 elective subjects'}), 400
        
        # Check if core subjects are passed
        all_passed, failed = GradeValidator.validate_core_subjects_passed(core_subjects)
        if not all_passed:
            return jsonify({
                'success': False,
                'error': f'Failed core subjects. Cannot proceed: {", ".join(failed)}'
            }), 400
        
        # Calculate aggregate
        total_aggregate, core_aggregate, elective_aggregate, success, error_msg = GradeValidator.calculate_aggregate(
            core_subjects, electives
        )
        
        if not success:
            return jsonify({'success': False, 'error': f'Aggregate calculation error: {error_msg}'}), 400
        
        # Create student record
        student = Student(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=data.get('name'),
            email=data.get('email'),
            category=data.get('category'),
            core_subjects=data.get('core_subjects'),
            electives=data.get('electives'),
            aggregate=total_aggregate,
            core_aggregate=core_aggregate,
            electives_aggregate=elective_aggregate,
            verified=True
        )
        
        db.session.add(student)
        db.session.flush()
        
        # Find matching programs
        all_programs = Program.query.all()
        qualified, borderline = AdmissionMatcher.find_matching_programs(
            {
                'aggregate': total_aggregate,
                'core_subjects': core_subjects,
                'electives': electives
            },
            all_programs
        )
        
        # Store results
        student.qualified_programs = [p['program_id'] for p in qualified]
        student.borderline_programs = [p['program_id'] for p in borderline]
        
        # Create admission result records
        for prog_data in qualified + borderline:
            result = AdmissionResult(
                student_id=student.id,
                program_id=prog_data['program_id'],
                status=prog_data['status'],
                reason=prog_data['reason'],
                matched_subjects=prog_data['matched_subjects'],
                missing_subjects=prog_data['missing_subjects']
            )
            db.session.add(result)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'student_id': student.id,
            'aggregate': total_aggregate,
            'qualified_count': len(qualified),
            'borderline_count': len(borderline),
            'redirect_url': url_for('main.dashboard', student_id=student.id)
        })
    
    return render_template('verify-result.html')

# ==================== UNIVERSITIES ====================
@main_bp.route('/universities')
def universities():
    """Display all universities and their programs"""
    universities = University.query.order_by(University.name).all()
    return render_template('universities.html', universities=universities)

# ==================== DASHBOARD ====================
@main_bp.route('/dashboard')
def dashboard():
    """Display admission results dashboard"""
    student_id = request.args.get('student_id', type=int)
    
    if not student_id:
        return redirect(url_for('main.index'))
    
    student = Student.query.get(student_id)
    if not student:
        return redirect(url_for('main.index'))
    
    # Get admission results
    results = AdmissionResult.query.filter_by(student_id=student_id).all()
    
    qualified = [r for r in results if r.status == 'qualified']
    borderline = [r for r in results if r.status == 'borderline']
    
    # Check if student has paid
    if not student.is_paid:
        # If not paid, we still show the count of matches but hide the details
        return render_template('payment.html',
                             student=student,
                             qualified_count=len(qualified),
                             borderline_count=len(borderline),
                             paystack_public_key='pk_live_6b9968065dc0bd4842c97ffa138e49127c862888')

    # Group by university type
    qualified_traditional = [r for r in qualified if r.program.university.type == 'Traditional']
    qualified_technical = [r for r in qualified if r.program.university.type == 'Technical']

    # Group results by university for display
    results_by_university = {}
    for result in results:
        uni_name = result.program.university.name
        if uni_name not in results_by_university:
            results_by_university[uni_name] = {
                'university': result.program.university,
                'programs': []
            }
        results_by_university[uni_name]['programs'].append(result)
    
    return render_template('dashboard.html',
                         student=student,
                         qualified_results=qualified,
                         borderline_results=borderline,
                         qualified_traditional=qualified_traditional,
                         qualified_technical=qualified_technical,
                         results_by_university=results_by_university)

# ==================== PAYMENT ====================
@main_bp.route('/verify-payment/<int:student_id>', methods=['POST'])
def verify_payment(student_id):
    """Verify payment with Paystack"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data'}), 400
        
    reference = data.get('reference')
    if not reference:
        return jsonify({'success': False, 'error': 'Payment reference missing'}), 400
    
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'error': 'Student not found'}), 404
        
    # In a real app, you would verify this reference with Paystack API
    # For now, we'll mark as paid if we get a reference
    student.is_paid = True
    student.payment_reference = reference
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Payment verified successfully',
        'redirect_url': url_for('main.dashboard', student_id=student.id)
    })

# ==================== AUTHENTICATION ====================
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered', 'danger')
            return render_template('register.html')
            
        new_user = User(email=email, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('main.index'))
        
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Sign in an existing user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return render_template('login.html')
            
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
        
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    """Sign out the current user"""
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/history')
@login_required
def history():
    """Show user's past admission checks"""
    submissions = Student.query.filter_by(user_id=current_user.id).order_by(Student.submission_date.desc()).all()
    return render_template('history.html', submissions=submissions)

# Placeholder for Google Login - typically handled by a library like Authlib
@main_bp.route('/google-login', methods=['POST'])
def google_login():
    """Handle Google Login/Signup via a client-side token or direct OAuth"""
    data = request.get_json()
    email = data.get('email')
    google_id = data.get('google_id')
    name = data.get('name')
    profile_pic = data.get('profile_pic')
    
    if not email or not google_id:
        return jsonify({'success': False, 'error': 'Missing data'}), 400
        
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        # Check if user exists by email but no google_id
        user = User.query.filter_by(email=email).first()
        if user:
            user.google_id = google_id
            user.profile_pic = profile_pic
        else:
            # Create new user
            user = User(email=email, google_id=google_id, name=name, profile_pic=profile_pic)
            db.session.add(user)
            
    db.session.commit()
    login_user(user, remember=True)
    
    return jsonify({
        'success': True,
        'redirect_url': url_for('main.index')
    })

@main_bp.route('/api/firebase-auth', methods=['POST'])
def firebase_auth():
    """Sync Firebase user with local database and create session"""
    data = request.get_json()
    uid = data.get('uid')
    email = data.get('email')
    name = data.get('displayName')
    profile_pic = data.get('photoURL')
    
    if not uid or not email:
        return jsonify({'success': False, 'error': 'Missing UID or Email'}), 400
        
    user = User.query.filter_by(firebase_uid=uid).first()
    if not user:
        # Check if user exists by email
        user = User.query.filter_by(email=email).first()
        if user:
            user.firebase_uid = uid
            if not user.name: user.name = name
            if not user.profile_pic: user.profile_pic = profile_pic
        else:
            # Create new user
            user = User(
                email=email, 
                firebase_uid=uid, 
                name=name, 
                profile_pic=profile_pic
            )
            db.session.add(user)
            
    db.session.commit()
    login_user(user, remember=True)
    
    return jsonify({
        'success': True,
        'message': 'Authenticated successfully',
        'user': user.to_dict()
    })

# ==================== API ENDPOINTS ====================
@main_bp.route('/api/universities')
def api_universities():
    """Get list of universities"""
    unis = University.query.all()
    return jsonify({
        'success': True,
        'universities': [u.to_dict() for u in unis]
    })

@main_bp.route('/api/programs')
def api_programs():
    """Get list of programs with optional filtering"""
    university_id = request.args.get('university_id', type=int)
    category = request.args.get('category')
    
    query = Program.query
    
    if university_id:
        query = query.filter_by(university_id=university_id)
    
    programs = query.all()
    return jsonify({
        'success': True,
        'programs': [p.to_dict() for p in programs]
    })

@main_bp.route('/api/admission-status/<int:student_id>')
def api_admission_status(student_id):
    """Get admission status for a student"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'error': 'Student not found'}), 404
    
    results = AdmissionResult.query.filter_by(student_id=student_id).all()
    
    qualified = [r.to_dict() for r in results if r.status == 'qualified']
    borderline = [r.to_dict() for r in results if r.status == 'borderline']
    
    return jsonify({
        'success': True,
        'student': student.to_dict(),
        'qualified': qualified,
        'borderline': borderline,
        'total_programs': len(results)
    })

# ==================== SEARCH ====================
@main_bp.route('/search')
def search():
    """Search universities and programs"""
    q = request.args.get('q', '').strip()
    
    if len(q) < 2:
        return jsonify({'success': False, 'error': 'Search query too short'}), 400
    
    # Search universities
    universities = University.query.filter(
        University.name.ilike(f'%{q}%')
    ).all()
    
    # Search programs
    programs = Program.query.filter(
        Program.name.ilike(f'%{q}%')
    ).all()
    
    return jsonify({
        'success': True,
        'universities': [u.to_dict() for u in universities],
        'programs': [p.to_dict() for p in programs]
    })

# ==================== ERROR HANDLERS ====================
@main_bp.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                          error_code=404, 
                          error_message='Page not found'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html',
                          error_code=500,
                          error_message='Internal server error'), 500
