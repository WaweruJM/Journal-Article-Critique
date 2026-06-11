// Article Critique Platform - Custom JavaScript
// Compatible with Radar app styling

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Article Critique Platform loaded');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    initializeSmoothScrolling();
    
    // Add file upload feedback
    initializeFileUploadFeedback();
});

// Tooltip initialization
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = element.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #0b3c5d;
                color: white;
                padding: 5px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            `;
            
            const rect = element.getBoundingClientRect();
            tooltip.style.top = `${rect.top - 30 + window.scrollY}px`;
            tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
            
            document.body.appendChild(tooltip);
            
            element.addEventListener('mouseleave', () => {
                tooltip.remove();
            }, { once: true });
        });
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// File upload feedback enhancement
function initializeFileUploadFeedback() {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const fileName = this.files[0].name;
                const fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
                
                // Show feedback message
                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'success-box';
                feedbackDiv.style.cssText = 'margin-top: 10px; padding: 10px;';
                feedbackDiv.innerHTML = `
                    ✅ File selected: <strong>${fileName}</strong> (${fileSize} MB)
                `;
                
                // Remove existing feedback
                const existing = document.querySelector('.file-feedback');
                if (existing) existing.remove();
                
                feedbackDiv.classList.add('file-feedback');
                fileInput.parentNode.appendChild(feedbackDiv);
            }
        });
    }
}

// Console greeting
console.log('%c📋 Journal Article Critique Platform | Research Quality Assessment', 'color: #0b3c5d; font-size: 14px; font-weight: bold;');
console.log('%cPowered by CASP, STROBE, CONSORT, PRISMA, SMART guidelines', 'color: #3498db; font-size: 12px;');
console.log('%c🔗 wawerujm.github.io', 'color: #0b3c5d; font-size: 12px;');