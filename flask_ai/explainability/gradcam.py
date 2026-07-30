import os
import cv2
import numpy as np


class GradCAM:

    def generate(self, image, output_path):

        """
        Placeholder for Grad-CAM generation.

        Replace this with actual Grad-CAM code
        after the CNN model is available.
        """

        heatmap = np.zeros(
            (image.shape[0], image.shape[1]),
            dtype=np.uint8
        )

        heatmap[:] = 120

        colored = cv2.applyColorMap(
            heatmap,
            cv2.COLORMAP_JET
        )

        overlay = cv2.addWeighted(
            image,
            0.6,
            colored,
            0.4,
            0
        )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        cv2.imwrite(
            output_path,
            overlay
        )

        return output_path


gradcam = GradCAM()