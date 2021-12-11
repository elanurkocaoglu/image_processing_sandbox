import numpy as np
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import os

from settings import *
from functions import iterate_and_detect_qrs


if __name__=="__main__":
    iterate_and_detect_qrs()