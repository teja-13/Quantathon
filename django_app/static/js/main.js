/**
 * Main Application JS Script
 */
document.addEventListener('DOMContentLoaded', function() {
    // Auto dismiss Bootstrap alert banners after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebar_toggle_btn');
    const sidebar = document.getElementById('app_sidebar');
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
});