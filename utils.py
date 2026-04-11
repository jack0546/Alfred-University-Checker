"""
Utility functions for Ghana Admission Checker
"""
import os
from werkzeug.utils import secure_filename
from config import Config
from PIL import Image

# Try to import optional OCR libraries
try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False

try:
    import pytesseract
    from PIL import Image
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

class GradeValidator:
    """Validate WASSCE grades and calculate aggregates"""
    
    VALID_GRADES = set(Config.GRADE_POINTS.keys())
    PASSING_GRADES = Config.PASSING_GRADES
    FAILING_GRADES = Config.FAILING_GRADES
    
    @staticmethod
    def is_valid_grade(grade):
        """Check if grade is valid WASSCE format"""
        return grade.upper() in GradeValidator.VALID_GRADES
    
    @staticmethod
    def is_passing_grade(grade):
        """Check if grade is a passing grade"""
        return grade.upper() in GradeValidator.PASSING_GRADES
    
    @staticmethod
    def grade_to_points(grade):
        """Convert grade to points"""
        grade_upper = grade.upper()
        if grade_upper in Config.GRADE_POINTS:
            return Config.GRADE_POINTS[grade_upper]
        return None
    
    @staticmethod
    def validate_subjects(subjects, required_subjects):
        """
        Validate that student has taken required subjects
        Returns: (is_valid, missing_subjects)
        """
        # Subject aliases and variations
        subject_aliases = {
            'mathematics': ['math', 'core mathematics', 'core maths'],
            'english': ['english language'],
            'science': ['integrated science'],
            'social studies': ['social studies', 'social'],
        }
        
        # Normalize student subject keys
        subject_keys = set()
        for subj in subjects.keys():
            subj_lower = subj.lower().strip()
            subject_keys.add(subj_lower)
            # Also add normalized versions
            for key, aliases in subject_aliases.items():
                if subj_lower in aliases or key in subj_lower:
                    subject_keys.add(key)
                    for alias in aliases:
                        subject_keys.add(alias)
        
        # Normalize required subjects
        required_keys = set()
        for subj in required_subjects:
            subj_lower = subj.lower().strip()
            required_keys.add(subj_lower)
            # Also normalize
            for key, aliases in subject_aliases.items():
                if subj_lower in aliases or key in subj_lower:
                    required_keys.add(key)
                    for alias in aliases:
                        required_keys.add(alias)
        
        # Find missing subjects
        missing = required_keys - subject_keys
        # Clean up missing list - only return meaningful ones
        missing_cleaned = []
        for m in missing:
            # Skip aliases, only return main subject names
            is_alias = False
            for main, aliases in subject_aliases.items():
                if m in aliases:
                    is_alias = True
                    break
            if not is_alias or m in ['english language', 'core mathematics', 'integrated science']:
                missing_cleaned.append(m)
        
        has_all_required = len(missing) == 0
        
        return has_all_required, list(set(missing_cleaned)) if missing_cleaned else list(missing)
    
    @staticmethod
    def validate_core_subjects_passed(core_subjects):
        """
        Check if all core subjects are passed
        Returns: (all_passed, failed_subjects)
        """
        failed = []
        for subject, grade in core_subjects.items():
            if not GradeValidator.is_passing_grade(grade):
                failed.append(subject)
        
        return len(failed) == 0, failed
    
    @staticmethod
    def calculate_aggregate(core_subjects, electives):
        """
        Calculate total aggregate from best 3 core subjects and best 3 electives
        Returns: (total_aggregate, core_aggregate, electives_aggregate, success, error_message)
        """
        try:
            # Validate core subjects
            if len(core_subjects) < 3:
                return None, None, None, False, f"Need at least 3 core subjects, got {len(core_subjects)}"
            
            # Validate electives
            if len(electives) < 3:
                return None, None, None, False, f"Need at least 3 electives, got {len(electives)}"
            
            # Check if all are valid grades
            all_subjects = {**core_subjects, **electives}
            for subject, grade in all_subjects.items():
                if not GradeValidator.is_valid_grade(grade):
                    return None, None, None, False, f"Invalid grade '{grade}' for {subject}"
            
            # Get points for all grades
            core_points = [GradeValidator.grade_to_points(g) for g in core_subjects.values()]
            electives_points = [GradeValidator.grade_to_points(g) for g in electives.values()]
            
            # Sort and get best 3 of each
            core_points_sorted = sorted(core_points)[:3]  # Lowest 3 (best)
            electives_points_sorted = sorted(electives_points)[:3]  # Lowest 3 (best)
            
            core_aggregate = sum(core_points_sorted)
            electives_aggregate = sum(electives_points_sorted)
            total_aggregate = core_aggregate + electives_aggregate
            
            return total_aggregate, core_aggregate, electives_aggregate, True, ""
            
        except Exception as e:
            return None, None, None, False, str(e)


class ResultSlipProcessor:
    """Handle result slip uploads and OCR processing"""
    
    @staticmethod
    def allowed_file(filename):
        """Check if file is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_upload_file(file):
        """Save uploaded file and return path"""
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        if file and ResultSlipProcessor.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            import time
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            return filepath
        
        return None
    
    @staticmethod
    def extract_text_from_image(image_path):
        """Extract text from image using OCR"""
        if not Config.USE_OCR:
            return None, "OCR is disabled"
        
        # Try EasyOCR first
        if HAS_EASYOCR:
            try:
                reader = easyocr.Reader(['en'])
                result = reader.readtext(image_path)
                text = '\n'.join([text for (bbox, text, confidence) in result])
                return text, None
            except Exception as e:
                return None, f"EasyOCR error: {str(e)}"
        
        # Fallback to Tesseract if available
        if HAS_TESSERACT:
            try:
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image)
                return text, None
            except Exception as e:
                return None, f"Tesseract error: {str(e)}"
        
        return None, "No OCR library available. Install easyocr or pytesseract."
    
    @staticmethod
    def parse_result_slip_text(text):
        """Parse extracted text to find name, category, subjects and grades - IMPROVED for real OCR"""
        import re
        
        lines = text.split('\n')
        parsed_data = {
            'name': '',
            'category': '',
            'core_subjects': {},
            'electives': {}
        }
        
        core_subjects_list = [
            'integrated science', 'social studies', 'core mathematics', 'core maths', 'mathematics',
            'english language', 'english', 'math', 'science', 
            'ict', 'information technology', 'computer studies'
        ]
        
        electives_list = [
            'further mathematics', 'additional mathematics', 'business studies',
            'technical drawing', 'civic education', 
            'physics', 'chemistry', 'biology', 'accounting', 'economics', 
            'geography', 'history', 'literature', 'french', 'government',
            'agriculture', 'computer science', 'design', 'visual arts', 'music'
        ]
        
        subjects_found = {}
        name_candidates = []
        parsing_core = False
        parsing_electives = False
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            if not line or len(line) < 2:
                continue
            
            # Detect section headers  
            if 'CORE' in line.upper() and ('SUBJECT' in line.upper() or 'COURSE' in line.upper()):
                parsing_core = True
                parsing_electives = False
                continue
            elif ('ELECTIVE' in line.upper() or 'OPTIONAL' in line.upper()) and 'SUBJECT' in line.upper():
                parsing_core = False
                parsing_electives = True
                continue
            
            # Enhanced name extraction - look for patterns with names
            if re.search(r'\b(name|surname)\b', line, re.IGNORECASE):
                # Try multiple patterns
                patterns = [
                    r'(?:name|surname)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                    r'(?:name|surname)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
                ]
                for pattern in patterns:
                    name_match = re.search(pattern, original_line)
                    if name_match:
                        extracted = name_match.group(1).strip()
                        if len(extracted) > 3:
                            name_candidates.append(extracted)
            
            # Look for grade patterns - flexible matching
            grade_pattern = r'([A-F])\s*([1-9])'
            grade_match = re.search(grade_pattern, line)
            
            if grade_match:
                grade = grade_match.group(1) + grade_match.group(2)
                subject_part = line[:grade_match.start()].strip()
                
                # Remove trailing pipes/dashes/separators
                subject_part = re.sub(r'[\|\-\s]+$', '', subject_part).strip()
                
                if subject_part and len(subject_part) > 2:
                    # Clean subject - remove noise
                    subject = re.sub(r'[^\w\s]', '', subject_part)
                    subject = ' '.join(subject.split()).strip()
                    
                    if len(subject) > 2 and subject not in subjects_found:
                        subject_lower = subject.lower()
                        
                        # Check for keywords
                        is_core_keyword = any(core.lower() in subject_lower for core in core_subjects_list)
                        is_elective_keyword = any(elec.lower() in subject_lower for elec in electives_list)
                        
                        # Section-based takes priority
                        if parsing_core:
                            subjects_found[subject] = (grade, True)
                        elif parsing_electives:
                            subjects_found[subject] = (grade, False)
                        else:
                            # Keyword matching
                            if is_elective_keyword and not is_core_keyword:
                                subjects_found[subject] = (grade, False)
                            elif is_core_keyword:
                                subjects_found[subject] = (grade, True)
                            else:
                                # Default to core if unknown
                                subjects_found[subject] = (grade, True)
        
        # Extract best name
        if name_candidates:
            # Filter and sort by legitimacy
            valid = [n for n in name_candidates if len(n) > 3 and not any(kw in n.upper() for kw in ['WASSCE', 'RESULT'])]
            parsed_data['name'] = valid[0] if valid else name_candidates[0]
        
        # Separate core and elective subjects
        core_count = 0
        elec_count = 0
        for subject, (grade, is_core) in subjects_found.items():
            if is_core and core_count < 5:
                parsed_data['core_subjects'][subject] = grade
                core_count += 1
            elif not is_core and elec_count < 5:
                parsed_data['electives'][subject] = grade
                elec_count += 1
        
        # Detect category based on electives
        elective_lower = [s.lower() for s in parsed_data['electives'].keys()]
        
        science_keywords = ['physics', 'chemistry', 'biology', 'further', 'additional']
        arts_keywords = ['literature', 'history', 'geography', 'french', 'government']
        business_keywords = ['accounting', 'economics', 'business']
        
        sci_score = sum(1 for s in elective_lower if any(k in s for k in science_keywords))
        arts_score = sum(1 for s in elective_lower if any(k in s for k in arts_keywords))
        biz_score = sum(1 for s in elective_lower if any(k in s for k in business_keywords))
        
        if sci_score >= 2:
            parsed_data['category'] = 'Science'
        elif arts_score >= 2:
            parsed_data['category'] = 'General Arts'
        elif biz_score >= 1:
            parsed_data['category'] = 'Business'
        else:
            parsed_data['category'] = 'Science'
        
        # Return if valid - be flexible with requirements for real OCR
        if len(parsed_data['core_subjects']) >= 2 and len(parsed_data['electives']) >= 2:
            return parsed_data
        
        return None


class AdmissionMatcher:
    """Match student results against program requirements"""
    
    @staticmethod
    def check_program_eligibility(student_data, program):
        """
        Check if student is eligible for program
        Returns: (status, reason, matched_subjects, missing_subjects)
        """
        try:
            core_subjects = student_data.get('core_subjects', {})
            electives = student_data.get('electives', {})
            
            # Check if student has required core subjects
            if program.required_core_subjects:
                has_required, missing = GradeValidator.validate_subjects(
                    core_subjects,
                    program.required_core_subjects
                )
                if not has_required:
                    return 'not_qualified', f"Missing required subjects: {', '.join(missing)}", None, missing
            
            # Check aggregate
            student_aggregate = student_data['aggregate']
            max_aggregate = program.maximum_aggregate
            
            # In Ghana system, LOWER aggregate is better (like golf scoring)
            if student_aggregate <= max_aggregate:
                status = 'qualified'
                reason = f"Aggregate: {student_aggregate} (Requirement: ≤{max_aggregate})"
            elif student_aggregate <= max_aggregate + 2:  # Borderline (within 2 points)
                status = 'borderline'
                reason = f"Aggregate: {student_aggregate} (Requirement: ≤{max_aggregate}) - Borderline"
            else:
                status = 'not_qualified'
                reason = f"Aggregate: {student_aggregate} exceeds requirement of ≤{max_aggregate}"
            
            return status, reason, list(core_subjects.keys()), []
            
        except Exception as e:
            return 'not_qualified', f"Error checking eligibility: {str(e)}", None, None
    
    @staticmethod
    def analyze_student_performance(student_data):
        """
        Analyze student performance to determine special admission rules
        Returns: (has_d_in_core, has_f_in_elective, aggregate_range, passes_core, passes_electives)
        """
        core_subjects = student_data.get('core_subjects', {})
        electives = student_data.get('electives', {})
        aggregate = student_data.get('aggregate', 0)
        
        # Check for D grades in core subjects
        has_d_in_core = any(grade.upper() in ['D7', 'E8'] for grade in core_subjects.values())
        
        # Check for F grades in electives
        has_f_in_elective = any(grade.upper() == 'F9' for grade in electives.values())
        
        # Check aggregate range
        aggregate_range = None
        if 27 <= aggregate <= 36:
            aggregate_range = 'high'  # High aggregate, less competitive
        
        # Check if student passes core subjects (at least 3 credits)
        core_passes = sum(1 for grade in core_subjects.values() if grade.upper() in ['A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        passes_core = core_passes >= 3
        
        # Check if student passes electives (at least 3 credits)
        elective_passes = sum(1 for grade in electives.values() if grade.upper() in ['A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        passes_electives = elective_passes >= 3
        
        return has_d_in_core, has_f_in_elective, aggregate_range, passes_core, passes_electives
    
    @staticmethod
    def find_matching_programs(student_data, programs):
        """Find all matching programs for student with special admission rules"""
        qualified = []
        borderline = []
        
        # Analyze student performance
        has_d_in_core, has_f_in_elective, aggregate_range, passes_core, passes_electives = AdmissionMatcher.analyze_student_performance(student_data)
        
        # Apply special admission rules
        for program in programs:
            status, reason, matched, missing = AdmissionMatcher.check_program_eligibility(student_data, program)
            
            # Apply special rules based on student performance
            modified_status = status
            
            # Rule 1: If aggregate 27-36, prefer less popular programs
            if aggregate_range == 'high':
                if program.popularity_level == 'low':
                    # Boost eligibility for less popular programs
                    if status == 'not_qualified' and student_data['aggregate'] <= program.maximum_aggregate + 3:
                        modified_status = 'qualified'
                        reason += " (Special consideration for less popular program)"
                    elif status == 'borderline':
                        modified_status = 'qualified'
                        reason += " (Preferred for less popular program)"
            
            # Rule 2: If D in core, prefer less valuable programs
            if has_d_in_core:
                if program.value_level == 'low':
                    # Boost eligibility for less valuable programs
                    if status == 'not_qualified' and student_data['aggregate'] <= program.maximum_aggregate + 2:
                        modified_status = 'qualified'
                        reason += " (Special consideration for less competitive program)"
            
            # Rule 3: If F in elective but passes core and electives, give desired programs
            if has_f_in_elective and passes_core and passes_electives:
                if program.is_desired_program:
                    # Boost eligibility for desired programs despite F in elective
                    if status == 'not_qualified' and student_data['aggregate'] <= program.maximum_aggregate + 4:
                        modified_status = 'qualified'
                        reason += " (Special consideration despite elective F grade)"
                    elif status == 'borderline':
                        modified_status = 'qualified'
                        reason += " (Eligible for desired program)"
            
            result = {
                'program_id': program.id,
                'program_name': program.name,
                'university_id': program.university_id,
                'university_name': program.university.name,
                'status': modified_status,
                'reason': reason,
                'matched_subjects': matched,
                'missing_subjects': missing,
                'university_type': program.university.type,
                'popularity_level': program.popularity_level,
                'value_level': program.value_level,
                'is_desired_program': program.is_desired_program
            }
            
            if modified_status == 'qualified':
                qualified.append(result)
            elif modified_status == 'borderline':
                borderline.append(result)
        
        return qualified, borderline
        
        for program in programs:
            status, reason, matched, missing = AdmissionMatcher.check_program_eligibility(student_data, program)
            
            result = {
                'program_id': program.id,
                'program_name': program.name,
                'university_id': program.university_id,
                'university_name': program.university.name,
                'status': status,
                'reason': reason,
                'matched_subjects': matched,
                'missing_subjects': missing,
                'university_type': program.university.type
            }
            
            if status == 'qualified':
                qualified.append(result)
            elif status == 'borderline':
                borderline.append(result)
        
        return qualified, borderline

