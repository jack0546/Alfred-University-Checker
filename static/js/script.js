/* Ghana Admission Checker - JavaScript */

// Utility Functions
const Utils = {
    showToast: function(message, type = 'info') {
        const toastHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        const container = document.querySelector('main') || document.body;
        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHtml;
        container.insertBefore(toastElement.firstElementChild, container.firstChild);
    },
    
    formatGradeTable: function(subjects) {
        if (!subjects || Object.keys(subjects).length === 0) {
            return '<p class="text-muted">No subjects</p>';
        }
        
        let html = '<table class="table table-sm"><tbody>';
        for (const [subject, grade] of Object.entries(subjects)) {
            html += `<tr><td>${subject}</td><td><span class="badge bg-primary">${grade}</span></td></tr>`;
        }
        html += '</tbody></table>';
        return html;
    },
    
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return email === '' || re.test(email);
    },
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// API Functions
const API = {
    uploadResult: async function(file) {
        const formData = new FormData();
        formData.append('result_slip', file);
        
        try {
            const response = await fetch('/upload-result', {
                method: 'POST',
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    },
    
    verifyResult: async function(data) {
        try {
            const response = await fetch('/verify-result', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Verification error:', error);
            throw error;
        }
    },
    
    getUniversities: async function() {
        try {
            const response = await fetch('/api/universities');
            return await response.json();
        } catch (error) {
            console.error('Error fetching universities:', error);
            throw error;
        }
    },
    
    search: async function(query) {
        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            return await response.json();
        } catch (error) {
            console.error('Search error:', error);
            throw error;
        }
    }
};

// WASSCE Grade Validation
const GradeValidator = {
    validGrades: ['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'E8', 'F9'],
    passingGrades: ['A1', 'B2', 'B3', 'C4', 'C5', 'C6'],
    gradePoints: {
        'A1': 1, 'B2': 2, 'B3': 3, 'C4': 4, 'C5': 5, 'C6': 6,
        'D7': 7, 'E8': 8, 'F9': 9
    },
    
    isValid: function(grade) {
        return this.validGrades.includes(grade.toUpperCase());
    },
    
    isPassing: function(grade) {
        return this.passingGrades.includes(grade.toUpperCase());
    },
    
    getPoints: function(grade) {
        return this.gradePoints[grade.toUpperCase()] || null;
    },
    
    calculateAggregate: function(coreSubjects, electives) {
        const grades = [...Object.values(coreSubjects), ...Object.values(electives)];
        const points = grades.map(g => this.getPoints(g)).sort((a, b) => a - b);
        
        const corePoints = Object.values(coreSubjects).map(g => this.getPoints(g)).sort((a, b) => a - b);
        const elecPoints = Object.values(electives).map(g => this.getPoints(g)).sort((a, b) => a - b);
        
        const coreAggregate = corePoints.slice(0, 3).reduce((a, b) => a + b, 0);
        const elecAggregate = elecPoints.slice(0, 3).reduce((a, b) => a + b, 0);
        const totalAggregate = coreAggregate + elecAggregate;
        
        return {
            total: totalAggregate,
            core: coreAggregate,
            elec: elecAggregate
        };
    }
};

// Initialize tooltips and popovers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Utility: Array of valid Ghanaian universities
const GHANAIAN_UNIVERSITIES = {
    traditional: [
        'University of Ghana',
        'Kwame Nkrumah University of Science and Technology',
        'University of Cape Coast',
        'University of Education Winneba',
        'University for Development Studies',
        'University of Mines and Technology',
        'University of Energy and Natural Resources'
    ],
    technical: [
        'Accra Technical University',
        'Koforidua Technical University',
        'Kumasi Technical University',
        'Takoradi Technical University',
        'Ho Technical University',
        'Sunyani Technical University',
        'Tamale Technical University',
        'Cape Coast Technical University',
        'Bolgatanga Technical University'
    ]
};

// Local Storage Utilities
const LocalStorage = {
    save: function(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('LocalStorage save error:', error);
            return false;
        }
    },
    
    get: function(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('LocalStorage get error:', error);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('LocalStorage remove error:', error);
            return false;
        }
    },
    
    clear: function() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('LocalStorage clear error:', error);
            return false;
        }
    }
};

// Session Storage Utilities
const SessionStorage = {
    save: function(key, data) {
        try {
            sessionStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('SessionStorage save error:', error);
            return false;
        }
    },
    
    get: function(key) {
        try {
            const data = sessionStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('SessionStorage get error:', error);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            sessionStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('SessionStorage remove error:', error);
            return false;
        }
    }
};

// Logging utility for debugging
const Logger = {
    log: function(message, data = null) {
        console.log(`[Ghana Admission Checker] ${message}`, data || '');
    },
    
    warn: function(message, data = null) {
        console.warn(`[Ghana Admission Checker] WARNING: ${message}`, data || '');
    },
    
    error: function(message, data = null) {
        console.error(`[Ghana Admission Checker] ERROR: ${message}`, data || '');
    }
};

// Export for use in other scripts
window.Utils = Utils;
window.API = API;
window.GradeValidator = GradeValidator;
window.LocalStorage = LocalStorage;
window.SessionStorage = SessionStorage;
window.Logger = Logger;
window.GHANAIAN_UNIVERSITIES = GHANAIAN_UNIVERSITIES;
