import cv2
import numpy as np


class ImagePreprocessor:

    IMAGE_SIZE = (224, 224)

    @staticmethod
    def preprocess(image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.resize(
            image,
            ImagePreprocessor.IMAGE_SIZE
        )

        image = image.astype(np.float32) / 255.0

        return image