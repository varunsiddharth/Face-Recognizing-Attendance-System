// Enhanced Animation and Interaction Scripts
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations
    initializeAnimations();
    initializeInteractions();
    initializePageTransitions();
});

// Initialize page animations
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.menu-item, .stat-card, .attendance-item, .form-group').forEach(el => {
        observer.observe(el);
    });

    // Add staggered animation to menu items
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
}

// Initialize interactive elements
function initializeInteractions() {
    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(-1px) scale(0.98)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
    });

    // Enhanced form interactions
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            this.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            this.style.transform = 'scale(1)';
        });
    });

    // Menu item hover effects
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) rotateX(5deg) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.2)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0deg) scale(1)';
            this.style.boxShadow = '0 8px 32px 0 rgba(31, 38, 135, 0.37)';
        });
    });

    // Table row interactions
    const tableRows = document.querySelectorAll('tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.backgroundColor = 'rgba(102, 126, 234, 0.05)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.backgroundColor = '';
        });
    });
}

// Initialize page transitions
function initializePageTransitions() {
    // Add loading animation for page transitions
    const links = document.querySelectorAll('a[href^="/"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add page transition effect
            document.body.style.opacity = '0.8';
            document.body.style.transform = 'scale(0.98)';
            
            setTimeout(() => {
                document.body.style.opacity = '1';
                document.body.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

// Enhanced status message animations
function showAnimatedStatus(message, type, duration = 3000) {
    const statusDiv = document.getElementById('status');
    const statusElement = document.createElement('div');
    statusElement.className = `status ${type} animated-status`;
    statusElement.textContent = message;
    
    // Add entrance animation
    statusElement.style.opacity = '0';
    statusElement.style.transform = 'translateY(-20px)';
    
    statusDiv.innerHTML = '';
    statusDiv.appendChild(statusElement);
    
    // Animate in
    requestAnimationFrame(() => {
        statusElement.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        statusElement.style.opacity = '1';
        statusElement.style.transform = 'translateY(0)';
    });
    
    // Auto remove after duration
    setTimeout(() => {
        statusElement.style.opacity = '0';
        statusElement.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            if (statusElement.parentNode) {
                statusElement.parentNode.removeChild(statusElement);
            }
        }, 500);
    }, duration);
}

// Enhanced progress bar animation
function animateProgressBar(progressElement, targetPercentage) {
    let currentPercentage = 0;
    const increment = targetPercentage / 50; // 50 steps for smooth animation
    
    const interval = setInterval(() => {
        currentPercentage += increment;
        if (currentPercentage >= targetPercentage) {
            currentPercentage = targetPercentage;
            clearInterval(interval);
        }
        
        progressElement.style.width = currentPercentage + '%';
        
        // Add pulsing effect when complete
        if (currentPercentage >= targetPercentage) {
            progressElement.style.animation = 'pulse 1s infinite';
        }
    }, 20);
}

// Enhanced camera preview effects
function initializeCameraEffects() {
    const video = document.getElementById('video');
    if (video) {
        video.addEventListener('loadedmetadata', function() {
            this.style.opacity = '0';
            this.style.transform = 'scale(0.9)';
            
            requestAnimationFrame(() => {
                this.style.transition = 'all 0.5s ease-out';
                this.style.opacity = '1';
                this.style.transform = 'scale(1)';
            });
        });
    }
}

// Enhanced recognition overlay animation
function showRecognitionOverlay(text, color = '#667eea') {
    const overlay = document.getElementById('recognitionOverlay');
    const textElement = document.getElementById('recognitionText');
    
    if (overlay && textElement) {
        textElement.textContent = text;
        textElement.style.color = color;
        overlay.classList.add('show');
        
        // Add pulsing animation
        textElement.style.animation = 'pulse 0.5s infinite';
        
        // Remove animation after 2 seconds
        setTimeout(() => {
            textElement.style.animation = '';
        }, 2000);
    }
}

// Enhanced attendance item animation
function addAttendanceItemWithAnimation(itemData) {
    const attendanceList = document.getElementById('attendanceList');
    if (!attendanceList) return;
    
    const itemElement = document.createElement('div');
    itemElement.className = 'attendance-item';
    itemElement.innerHTML = `
        <div class="student-info">${itemData.name} (ID: ${itemData.id})</div>
        <div class="time">${itemData.time}</div>
    `;
    
    // Add entrance animation
    itemElement.style.opacity = '0';
    itemElement.style.transform = 'translateX(30px)';
    attendanceList.insertBefore(itemElement, attendanceList.firstChild);
    
    // Animate in
    requestAnimationFrame(() => {
        itemElement.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        itemElement.style.opacity = '1';
        itemElement.style.transform = 'translateX(0)';
    });
    
    // Add success flash effect
    itemElement.style.background = 'linear-gradient(135deg, #c6f6d5, #9ae6b4)';
    setTimeout(() => {
        itemElement.style.background = '';
    }, 1000);
}

// Enhanced table animations
function animateTableData(tableBody, data) {
    const rows = tableBody.querySelectorAll('tr');
    rows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            row.style.transition = 'all 0.3s ease-out';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// Enhanced form validation with animations
function validateFormWithAnimation(formElement) {
    const inputs = formElement.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#f56565';
            input.style.transform = 'shake 0.5s ease-in-out';
            
            // Add shake animation
            input.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                input.style.animation = '';
            }, 500);
        } else {
            input.style.borderColor = '#48bb78';
            input.style.transform = 'scale(1.02)';
            setTimeout(() => {
                input.style.transform = 'scale(1)';
            }, 200);
        }
    });
    
    return isValid;
}

// Add CSS for shake animation
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .animate-in {
        animation: slideInUp 0.6s ease-out forwards;
    }
    
    .focused {
        transform: scale(1.02);
    }
    
    .animated-status {
        animation: slideInDown 0.5s ease-out;
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.AnimationUtils = {
    showAnimatedStatus,
    animateProgressBar,
    initializeCameraEffects,
    showRecognitionOverlay,
    addAttendanceItemWithAnimation,
    animateTableData,
    validateFormWithAnimation
};
