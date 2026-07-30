import cv2


def read_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to load image.")

    return image


def resize_image(image, size=(224, 224)):

    return cv2.resize(image, size)