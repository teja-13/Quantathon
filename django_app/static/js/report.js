/**
 * Report Printing & Actions
 */
function printMedicalReport() {
    window.print();
}

function simulatePDFDownload(reportNumber) {
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-bg-primary border-0 show position-fixed bottom-0 end-0 m-3';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-file-earmark-pdf me-2">
                Downloading Medical Report ${reportNumber} PDF...
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}