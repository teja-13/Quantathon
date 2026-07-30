ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "bmp",
    "tif",
    "tiff",
}

SUPPORTED_CANCERS = {
    "brain",
    "breast",
    "colon",
    "liver",
    "lung",
}


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


def validate_cancer_type(cancer_type):

    return cancer_type.lower() in SUPPORTED_CANCERS