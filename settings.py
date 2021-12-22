import cv2 as cv
import numpy as np

BG_DIR_PATH = "qrs_with_background"

QR_CASCADE = cv.CascadeClassifier("cascades/qr_cascade.xml")
PADDING = 50

FONT_FACE = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
THICKNESS = 2

QR_COLOR = (32, 32, 32)
MOTION_COLOR = (78, 255, 78)

MOTION_TEXT = "Motion Detected"

GAUSSIAN_KERNEL_SIZE = (7, 7)
MIN_CONTOUR_AREA = 200