import cv2 as cv

QR_CASCADE = cv.CascadeClassifier("cascades/qr_cascade.xml")
PADDING = 50

BG_DIR_PATH = "qrs_with_background"

QR_WIDTH = 15*0.393700787 # cm to inches