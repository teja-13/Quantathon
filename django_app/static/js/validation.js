/**
 * Client-Side Validation Utilities
 */
function validateImageFile(file) {
    const errorBox = document.getElementById('validation_error_box');
    if (errorBox) {
        errorBox.classList.add('d-none');
        errorBox.textContent = '';
    }

    const fileName = file.name.toLowerCase();
    const validExtensions = ['.jpg', '.jpeg', '.png', '.nii', '.nii.gz'];
    const hasValidExt = validExtensions.some(ext => fileName.endsWith(ext));

    if (!hasValidExt) {
        showValidationError('Invalid file format. Only JPG, JPEG, PNG, and NIfTI (.nii/.nii.gz) files are allowed.');
        return false;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB limit
    if (file.size > maxSize) {
        showValidationError('File size exceeds maximum allowed limit of 5MB.');
        return false;
    }

    return true;
}

function showValidationError(message) {
    const errorBox = document.getElementById('validation_error_box');
    if (errorBox) {
        errorBox.textContent = message;
        errorBox.classList.remove('d-none');
    } else {
        alert(message);
    }
}
