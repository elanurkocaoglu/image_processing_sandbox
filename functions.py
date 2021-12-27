from cv2 import dilate
import numpy as np
import pyzbar.pyzbar as pyzbar

import os
import datetime
import time
import imutils

from settings import *


def record_qr(qr_map: dict, qr_code: pyzbar.Decoded) -> None:
    """
        @brief record_qr does record decoded qr codes, if the timeout is reached,
        it can be re-detected
        @param qr_map: `dict` keys (data) and values (timestamps)
        @param qr_code: detected and decoded qr code object
    """
    byte_data = qr_code.data
    text_data = byte_data.decode("UTF-8")
    timestamp_now = datetime.datetime.now().timestamp()

    if text_data in qr_map.keys():
        timestamp_last = qr_map[text_data]
        if timestamp_now - timestamp_last > QR_DETECT_TIMEOUT:
            qr_map[text_data] = timestamp_now

    else:
        qr_map[text_data] = timestamp_now        


def detect_qr_and_print(frame: np.ndarray, gray: np.ndarray, qr_map: dict, cascade: cv.CascadeClassifier = QR_CASCADE) -> None:
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
            record_qr(qr_map, decoded_qr)

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


def detect_motion_and_print(frame: np.ndarray, gray: np.ndarray, previous_gray: np.ndarray) -> tuple:
    """
        @brief detect_motion_and_print does detect motion by using the difference between the previous frame and the current frame
        and shows it on the output frame
        @param frame: `np.ndarray` frame read from the camera, used for showing the motion
        @param gray: `np.ndarray` frame converted to gray scale, which is the current frame
        @param previous_gray `np.ndarray` frame converted to gray scale, which is the previously processed frame
        @return `np.ndarray`, diff frame (motion detected); `np.ndarray`, current gray scaled frame, which wil be used in the next
        iterations (a new frame is read from camera)
    """
    gaussian = cv.GaussianBlur(gray, GAUSSIAN_KERNEL_SIZE, 0)
    diff = cv.absdiff(previous_gray, gaussian)
    _, thresh = cv.threshold(diff, 50, 255, cv.THRESH_BINARY)
    thresh = cv.dilate(thresh, None, iterations=4)

    cv.imshow("Thresh", thresh)
    cv.waitKey(10)

    contours = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        if cv.contourArea(contour) < MIN_CONTOUR_AREA:
            continue

        else:
            #cv.drawContours(frame, contour, -1, MOTION_COLOR, THICKNESS*2)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x+w, y+h), MOTION_COLOR, THICKNESS)
            cv.putText(frame, MOTION_TEXT, (10, 40), FONT_FACE, FONT_SCALE, MOTION_COLOR, THICKNESS)

    previous_gray = gray

    return diff, previous_gray
