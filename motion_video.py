import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

from settings import *
from functions import detect_motion_and_print


if __name__ == "__main__":
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    ret, prev_frame = cap.read()
    prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    prev_gray = cv.GaussianBlur(prev_gray, GAUSSIAN_KERNEL_SIZE, 0)

    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        diff_frame, prev_gray = detect_motion_and_print(frame, gray, prev_gray)

        cv.imshow('Motion Detection', diff_frame)
        cv.imshow('Original', frame)
        cv.imshow('Gray', gray)

        if cv.waitKey(33) == ord("q") or cv.waitKey(40) == ord("Q"):
            break

    cap.release()
    cv.destroyAllWindows()