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

    function handleFileSelect(file) {
        if (!file) return;
        
        // Client-side extension & size validation check
        if (typeof validateImageFile === 'function' && !validateImageFile(file)) {
            fileInput.value = '';
            if (previewContainer) previewContainer.classList.add('d-none');
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