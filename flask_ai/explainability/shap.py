import os
import cv2


class SHAPGenerator:

    def generate(self, image, output_path):

        """
        Placeholder for SHAP explanation.

        Later replace with actual SHAP code.
        """

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        cv2.imwrite(
            output_path,
            image
        )

        return output_path


shap_generator = SHAPGenerator()