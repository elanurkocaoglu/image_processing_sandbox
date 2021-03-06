import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

from settings import *
from functions import detect_qr_and_print


if __name__ == "__main__":
    qr_map = dict()
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        detect_qr_and_print(frame, gray, qr_map)

        cv.imshow('Qr Detection', frame)
        cv.imshow('Qr Gray', gray)

        if cv.waitKey(20) == ord("q") or cv.waitKey(20) == ord("Q"):
            break

    for key in qr_map.keys():
        print(f"[*] {qr_map.get(key)} - {key}")

    cap.release()
    cv.destroyAllWindows()