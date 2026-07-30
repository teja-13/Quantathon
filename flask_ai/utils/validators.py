ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "bmp",
    "tif",
    "tiff",
    "nii",
}

SUPPORTED_CANCERS = {
    "brain",
    "breast",
    "liver",
    "lung",
    "kidney",
}


def allowed_file(filename):
    if "." not in filename:
        return False
    lower = filename.lower()
    if lower.endswith(".nii.gz"):
        return True
    extension = lower.rsplit(".", 1)[1]
    return extension in ALLOWED_EXTENSIONS


def validate_cancer_type(cancer_type):
    return cancer_type.lower() in SUPPORTED_CANCERS