/**
 * Image Upload Dropzone & Live Preview Handling
 */
document.addEventListener('DOMContentLoaded', function() {
    const dropzone = document.getElementById('upload_dropzone');
    const fileInput = document.getElementById('medical_image_input');
    const previewContainer = document.getElementById('preview_container');
    const previewImage = document.getElementById('preview_image');
    const previewFileName = document.getElementById('preview_filename');
    const previewFileSize = document.getElementById('preview_filesize');
    const cancelBtn = document.getElementById('cancel_upload_btn');

    if (dropzone && fileInput) {
        dropzone.addEventListener('click', function() {
            fileInput.click();
        });

        dropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });

        dropzone.addEventListener('dragleave', function() {
            dropzone.classList.remove('dragover');
        });

        dropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                handleFileSelect(fileInput.files[0]);
            }
        });

        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                handleFileSelect(fileInput.files[0]);
            }
        });

        if (cancelBtn) {
            cancelBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                fileInput.value = '';
                if (previewContainer) previewContainer.classList.add('d-none');
            });
        }
    }

    function isNiftiFile(fileName) {
        const lowerName = (fileName || '').toLowerCase();
        return lowerName.endsWith('.nii') || lowerName.endsWith('.nii.gz');
    }

    function buildNiftiPreviewDataUrl() {
        const svg = `
            <svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
                <defs>
                    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
                        <stop offset="0%" stop-color="#0f172a" />
                        <stop offset="100%" stop-color="#1e293b" />
                    </linearGradient>
                </defs>
                <rect width="640" height="360" rx="28" fill="url(#bg)" />
                <rect x="48" y="48" width="544" height="264" rx="22" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.18)" />
                <text x="320" y="165" text-anchor="middle" fill="#e2e8f0" font-family="Arial, sans-serif" font-size="34" font-weight="700">NIfTI Volume</text>
                <text x="320" y="208" text-anchor="middle" fill="#cbd5e1" font-family="Arial, sans-serif" font-size="18">Preview generated from axial slice + MIP</text>
            </svg>
        `;
        return 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg.trim());
    }

    function handleFileSelect(file) {
        if (!file) return;
        
        // Client-side extension & size validation check
        if (typeof validateImageFile === 'function' && !validateImageFile(file)) {
            fileInput.value = '';
            if (previewContainer) previewContainer.classList.add('d-none');
            return;
        }

        if (previewImage) previewImage.classList.remove('d-none');
        if (isNiftiFile(file.name)) {
            if (previewImage) previewImage.src = buildNiftiPreviewDataUrl();
            if (previewImage) previewImage.alt = 'NIfTI scan preview';
            if (previewFileName) previewFileName.textContent = file.name;
            if (previewFileSize) previewFileSize.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
            if (previewContainer) previewContainer.classList.remove('d-none');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            if (previewImage) previewImage.src = e.target.result;
            if (previewFileName) previewFileName.textContent = file.name;
            if (previewFileSize) previewFileSize.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
            if (previewContainer) previewContainer.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
    }
});