/**
 * Chart.js Integration for Medical Analytics
 */
function initDashboardCharts(labels, data) {
    const ctxDistribution = document.getElementById('cancerDistributionChart');
    if (ctxDistribution) {
        new Chart(ctxDistribution, {
            type: 'doughnut',
            data: {
                labels: labels || ['Brain Cancer', 'Breast Cancer', 'Lung Cancer', 'Liver Cancer', 'Kidney Cancer'],
                datasets: [{
                    data: data || [12, 19, 15, 8, 10],
                    backgroundColor: [
                        '#1565C0',
                        '#E91E63',
                        '#009688',
                        '#FF9800',
                        '#9C27B0'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { family: 'Inter', size: 12 } }
                    }
                },
                cutout: '70%'
            }
        });
    }

    const ctxMonthly = document.getElementById('monthlyScansChart');
    if (ctxMonthly) {
        new Chart(ctxMonthly, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Medical Scans Processed',
                    data: [28, 35, 42, 58, 64, 71, 85],
                    backgroundColor: '#1565C0',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#F0F4F8' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}