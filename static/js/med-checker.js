// med-checker.js - Real-time medication checking
// Place this file in: static/js/med-checker.js

/**
 * Debounce function to limit API calls
 * Waits for user to stop typing before checking
 */
function debounce(func, wait) {
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

/**
 * Get all currently entered medications
 * Returns array of {name, doses_per_day}
 */
function getCurrentMedications() {
    const medications = [];
    const medicationRows = document.querySelectorAll('.medication-row');
    
    medicationRows.forEach(row => {
        const nameInput = row.querySelector('input[name^="medication_name"]');
        const dosesInput = row.querySelector('input[name^="doses_per_day"]');
        
        if (nameInput && nameInput.value.trim()) {
            medications.push({
                name: nameInput.value.trim(),
                doses_per_day: parseInt(dosesInput?.value || 1)
            });
        }
    });
    
    return medications;
}

/**
 * Get patient age from form
 */
function getPatientAge() {
    const ageInput = document.getElementById('age') || document.querySelector('input[name="age"]');
    return parseInt(ageInput?.value || 65);
}

/**
 * Check medication in real-time
 * Called when user enters/changes a medication name
 */
async function checkMedicationRealtime(inputElement) {
    const medicationName = inputElement.value.trim();
    
    // Get the warning container for this specific row
    const medicationRow = inputElement.closest('.medication-row');
    let warningContainer = medicationRow.querySelector('.live-warning-container');
    
    // Create warning container if it doesn't exist
    if (!warningContainer) {
        warningContainer = document.createElement('div');
        warningContainer.className = 'live-warning-container';
        medicationRow.appendChild(warningContainer);
    }
    
    // Clear warnings if input is empty
    if (!medicationName) {
        warningContainer.innerHTML = '';
        warningContainer.style.display = 'none';
        return;
    }
    
    // Show loading state
    warningContainer.innerHTML = '<div class="checking-loader"><i class="fas fa-spinner fa-spin"></i> Checking...</div>';
    warningContainer.style.display = 'block';
    
    try {
        // Get all existing medications (excluding the current one being edited)
        const allMeds = getCurrentMedications();
        const existingMeds = allMeds.filter(med => 
            med.name.toLowerCase() !== medicationName.toLowerCase()
        );
        
        const response = await fetch('/api/check-medication', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                medication_name: medicationName,
                existing_medications: existingMeds,
                age: getPatientAge()
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayWarnings(warningContainer, data.warnings, data.safe);
            
            // Update row styling based on severity
            updateRowStyling(medicationRow, data.warnings);
        } else {
            warningContainer.innerHTML = `<div class="warning-error">Error checking medication</div>`;
        }
        
    } catch (error) {
        console.error('Error checking medication:', error);
        warningContainer.innerHTML = `<div class="warning-error">Unable to check medication</div>`;
    }
}

/**
 * Display warnings in the container
 */
function displayWarnings(container, warnings, isSafe) {
    if (!warnings || warnings.length === 0) {
        if (isSafe) {
            container.innerHTML = `
                <div class="warning-safe">
                    <i class="fas fa-check-circle"></i> No immediate concerns detected
                </div>
            `;
            setTimeout(() => {
                container.style.display = 'none';
            }, 2000);
        } else {
            container.style.display = 'none';
        }
        return;
    }
    
    // Build HTML for all warnings
    const warningsHTML = warnings.map(warning => {
        const severityClass = `warning-${warning.severity}`;
        
        return `
            <div class="live-warning ${severityClass}">
                <div class="warning-header">
                    <span class="warning-icon">${warning.icon}</span>
                    <span class="warning-title">${warning.title}</span>
                    <span class="warning-severity-badge">${warning.severity.toUpperCase()}</span>
                </div>
                <div class="warning-body">
                    <p class="warning-message">${warning.message}</p>
                    ${warning.recommendation ? `
                        <p class="warning-recommendation">
                            <strong>Recommendation:</strong> ${warning.recommendation}
                        </p>
                    ` : ''}
                    ${warning.category ? `
                        <p class="warning-category">
                            <strong>Category:</strong> ${warning.category}
                        </p>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = warningsHTML;
    container.style.display = 'block';
    
    // Animate in
    const warningElements = container.querySelectorAll('.live-warning');
    warningElements.forEach((el, index) => {
        el.style.animation = `slideInWarning 0.3s ease-out ${index * 0.1}s both`;
    });
}

/**
 * Update medication row styling based on warnings
 */
function updateRowStyling(row, warnings) {
    // Remove existing severity classes
    row.classList.remove('has-high-warning', 'has-moderate-warning', 'has-low-warning', 'is-safe');
    
    if (!warnings || warnings.length === 0) {
        row.classList.add('is-safe');
        return;
    }
    
    // Find highest severity
    const hasHigh = warnings.some(w => w.severity === 'high');
    const hasModerate = warnings.some(w => w.severity === 'moderate');
    
    if (hasHigh) {
        row.classList.add('has-high-warning');
    } else if (hasModerate) {
        row.classList.add('has-moderate-warning');
    } else {
        row.classList.add('has-low-warning');
    }
}

/**
 * Initialize real-time checking for all medication inputs
 */
function initializeMedicationChecker() {
    // Create debounced version (waits 800ms after user stops typing)
    const debouncedCheck = debounce(checkMedicationRealtime, 800);
    
    // Attach to existing medication name inputs
    document.querySelectorAll('input[name^="medication_name"]').forEach(input => {
        // Check on blur (when user leaves the field)
        input.addEventListener('blur', function() {
            checkMedicationRealtime(this);
        });
        
        // Also check while typing (debounced)
        input.addEventListener('input', function() {
            debouncedCheck(this);
        });
    });
    
    console.log('Real-time medication checker initialized');
}

/**
 * Re-initialize checker when new medication rows are added
 * Call this function after adding new medication rows dynamically
 */
function reinitializeMedicationChecker() {
    initializeMedicationChecker();
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMedicationChecker);
} else {
    initializeMedicationChecker();
}

// Export functions for use in other scripts
window.MedChecker = {
    check: checkMedicationRealtime,
    reinitialize: reinitializeMedicationChecker,
    getCurrentMedications: getCurrentMedications
};