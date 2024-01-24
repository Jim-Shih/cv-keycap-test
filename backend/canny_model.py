import cv2
import numpy as np


def read_image(image_path, mode=0):
    """Read image from path, default mode is 0 (grayscale)"""
    img = cv2.imread(image_path, mode)
    print("image shape: ", img.shape[:2])
    return img


def cropping_image(image, x, y, w, h):
    """Cropping image"""
    cropped = image[y:y + h, x:x + w]
    return cropped


def image_blurred(image, kernel_size=3):
    """Blurred image, default kernel size is (3,3)"""
    filtering_kernel = (np.ones(
        (kernel_size, kernel_size), np.float32) / kernel_size**2)
    blurred = cv2.filter2D(image, -1, filtering_kernel)
    return blurred


def canny_edge_detection(image):
    """Canny edge detection"""
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    return edges


if __name__ == "__main__":
    image_path = "keycapimage.jpg"

    image = read_image(image_path)
    y, x = image.shape[:2]
    cropped = cropping_image(image, 0, 0, x // 2, y)
    cropped_blurred = image_blurred(cropped, kernel_size=4)
    edges = canny_edge_detection(cropped_blurred)
    cv2.imshow("Canny", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
