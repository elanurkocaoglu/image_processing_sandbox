import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
qr_cascade = cv.CascadeClassifier("C:\\Users\\elanu\\Documents\\pandn\\classifier\\cascade.xml")
PADDING = 30

def filterImage(gray):
    filtered_gray = None
    return filtered_gray

def detectAndPrint(frame, gray, cascade=qr_cascade):
    qrcodes = cascade.detectMultiScale(gray, 2.6213145, 8)

    for (x, y, w, h) in qrcodes:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)
        cv.rectangle(frame, (x - 30, y - 30), (x+w+30, y+h+30), (127, 0, 255), 2)

        roi = gray[y-PADDING:y+h+PADDING, x-PADDING:x+w+PADDING]

        try:
            qrs = pyzbar.decode(roi)
            decoded_qr = qrs[0]
            byte_data = decoded_qr.data
            text_data = byte_data.decode("UTF-8")

            top = decoded_qr.rect.top
            left = decoded_qr.rect.left
            cv.putText(frame, text_data, (x-PADDING+left, y-PADDING+top),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        except: pass

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    filtered_gray = filterImage(gray)
    detectAndPrint(frame, gray)

    cv.imshow('Qr Detection', frame)
    cv.imshow('Qr Gray', gray)

    if cv.waitKey(20) == ord("q") or cv.waitKey(20) == ord("Q"):
        break

cap.release()
cv.destroyAllWindows()