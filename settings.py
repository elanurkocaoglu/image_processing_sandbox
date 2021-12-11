import cv2 as cv

QR_CASCADE = cv.CascadeClassifier("cascades/qr_cascade.xml")
PADDING = 50

BG_DIR_PATH = "qrs_with_background"