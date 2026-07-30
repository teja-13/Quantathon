/**
 * Processing Page Animated Pipeline Progress & Auto-Redirect
 */
document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.getElementById('processing_progress_bar');
    const stepItems = document.querySelectorAll('.processing-step-item');
    const redirectUrl = document.getElementById('redirect_url_target')?.value;

    if (progressBar && stepItems.length > 0 && redirectUrl) {
        let currentStep = 0;
        const totalSteps = stepItems.length;
        
        const stepInterval = setInterval(function() {
            if (currentStep < totalSteps) {
                // Update Step UI
                stepItems.forEach((item, index) => {
                    if (index <= currentStep) {
                        item.classList.add('active');
                        const statusIcon = item.querySelector('.step-status-icon');
                        if (statusIcon) {
                            statusIcon.className = 'bi bi-check-circle-fill text-success step-status-icon';
                        }
                    }
                });
                
                // Update Progress bar percentage
                const percent = Math.round(((currentStep + 1) / totalSteps) * 100);
                progressBar.style.width = percent + '%';
                progressBar.textContent = percent + '%';
                
                currentStep++;
            } else {
                clearInterval(stepInterval);
                setTimeout(function() {
                    window.location.href = redirectUrl;
                }, 800);
            }
        }, 900);
    }
});
