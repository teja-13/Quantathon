import numpy as np


def calculate(probabilities):

    return round(
        float(np.max(probabilities)) * 100,
        2
    )