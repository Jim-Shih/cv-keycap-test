import base64
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from fastapi import HTTPException


def check_if_its_base64(url: str):
    """check if the image is base64 encoded"""
    if url.startswith("data:image"):
        return True
    else:
        return False


def decode_base64_to_image(base64_string: str):
    # Convert Base64 string to bytes
    base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)

    # Create image object from byte data
    image = Image.open(BytesIO(image_bytes))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image


def receiving_image(message: str):
    img = None
    if (message is None) or (not check_if_its_base64(message)):
        raise HTTPException(status_code=400, detail="Please provide base64_string")
    print("received base64_string: ", message[:10])
    # decode the image from base64 to normal image
    img = decode_base64_to_image(message)
    return img


def encode_image_to_base64(image):
    """encode the image to base64"""
    _, buffer = cv2.imencode(".png", image)
    img_str = base64.b64encode(buffer)
    return img_str
