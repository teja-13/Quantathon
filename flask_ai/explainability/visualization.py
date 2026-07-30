import cv2


def overlay_text(
    image,
    text
):

    image = image.copy()

    cv2.putText(

        image,

        text,

        (20, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        (0, 255, 0),

        2

    )

    return image