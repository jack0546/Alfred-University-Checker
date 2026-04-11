"""
Utility functions for Ghana Admission Checker
"""
import os
from werkzeug.utils import secure_filename
from config import Config

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

