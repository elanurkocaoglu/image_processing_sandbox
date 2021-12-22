import numpy as np
import pyzbar.pyzbar as pyzbar

import os
import datetime
import time
import imutils

from settings import *


def detect_qr_and_print(frame: np.ndarray, gray: np.ndarray, cascade: cv.CascadeClassifier = QR_CASCADE) -> None:
    """
        @brief detect_qr_and_print does detect qr code in a `frame` (if any), then decodes it
        @param frame: `np.ndarray` frame read from the camera, used for printing the decoded qr
        @param gray: `np.darray` frame converted to gray scale, used for detection and decode
        @param cascade: `cv.CascadeClassifier` cascade in which the detection will be done
    """
    qrcodes = cascade.detectMultiScale(gray, 2.6213145, 4, maxSize=np.shape(gray))

    for (x, y, w, h) in qrcodes:
        roi = gray[y-PADDING:y+h+PADDING, x-PADDING:x+w+PADDING]

        try:
            qrs = pyzbar.decode(roi)
            decoded_qr = qrs[0]
            byte_data = decoded_qr.data
            text_data = byte_data.decode("UTF-8")

            top = decoded_qr.rect.top
            left = decoded_qr.rect.left

            width = decoded_qr.rect.width
            height = decoded_qr.rect.height

            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2) # raw detection
            cv.rectangle(frame, (x-PADDING, y-PADDING), (x+w+PADDING, y+h+PADDING), (127, 0, 255), 2) # padded region of interest
            cv.rectangle(frame, (x+left-PADDING, y+top-PADDING), (x+left+width-PADDING, y+top+height-PADDING), (213, 231, 76), 2) # detected qr

            cv.putText(frame, text_data, (x-PADDING+left, y-PADDING+top), FONT_FACE, FONT_SCALE, QR_COLOR, THICKNESS)
            print(f"[x] {datetime.datetime.now().timestamp()} - {text_data}")

        except: pass


def iterate_and_detect_qrs(dir_path: str = BG_DIR_PATH) -> None:
    """
        @brief iterate_and_detect_qrs does detect qr code (if any) and decode it on image files (for testing)
        @param dir_path: `str` path of directory
    """
    for img_path in os.listdir(BG_DIR_PATH):
        img = cv.imread(os.path.join(dir_path, img_path))
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        detect_qr_and_print(img, gray)
        time.sleep(1)


def detect_motion_and_print(frame: np.ndarray, gray: np.ndarray, previous_gray: np.ndarray):
    """
        @brief detect_motion_and_print does detect motion by using the difference between the previous frame and the current frame
        and shows it on the output frame
        @param frame: `np.ndarray` frame read from the camera, used for showing the motion
        @param gray: `np.ndarray` frame converted to gray scale, which is the current frame
        @param previous_gray `np.ndarray` frame converted to gray scale, which is the previously processed frame
    """
    gaussian = cv.GaussianBlur(gray, GAUSSIAN_KERNEL_SIZE, 0)
    thresh = cv.absdiff(previous_gray, gaussian)
    _, diff = cv.threshold(thresh, 50, 255, cv.THRESH_BINARY)

    contours = cv.findContours(diff, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        if cv.contourArea(contour) < MIN_CONTOUR_AREA:
            continue

        else:
            cv.drawContours(frame, contour, -1, MOTION_COLOR, THICKNESS*2)
            cv.putText(frame, MOTION_TEXT, (10, 40), FONT_FACE, FONT_SCALE, MOTION_COLOR, THICKNESS)

    previous_gray = gray

    return diff, previous_gray
