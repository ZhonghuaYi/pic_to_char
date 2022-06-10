# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-10
import sys

from Pic import Pic
import cv2 as cv
from PicProcess import PicProcess


class GrayPic(Pic):
    def __init__(self, image):
        """Make sure self.image is a 2-d ndarray object."""
        self.image = None
        super().__init__(image)
        self.image = PicProcess.image_to_gray(self.image)


class BinaryPic(GrayPic):
    def __init__(self, image, method=0, thresh=-1):
        self.image = None
        self.th = None
        super().__init__(image)
        try:
            if method == 0:
                self.th, self.image = cv.threshold(
                    self.image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            elif method == 1:
                if thresh <= 0 or thresh >= 255:
                    raise ValueError(
                        f"Wrong input variable: 'thresh'={thresh}")
                self.th, self.image = cv.threshold(self.image, thresh, 255,
                                                   cv.THRESH_BINARY)
            elif method == 1:
                self.image = cv.adaptiveThreshold(self.gray, 255,
                                                  cv.ADAPTIVE_THRESH_MEAN_C,
                                                  cv.THRESH_BINARY, 5, 0)
                self.th = -1
            else:
                raise ValueError(f"Wrong input variable: 'method'={method}")
        except Exception as e:
            print(e)
            sys.exit()

    def resize(self, size=(0, 0), fx=1., fy=1.):
        super().resize(size=size, fx=fx, fy=fy)
        if 0 < self.th < 255:
            _, self.image = cv.threshold(self.image, self.th, 255,
                                         cv.THRESH_BINARY)
        elif self.th == -1:
            self.image = cv.adaptiveThreshold(self.gray, 255,
                                              cv.ADAPTIVE_THRESH_MEAN_C,
                                              cv.THRESH_BINARY, 5, 0)


class EdgePic(BinaryPic):
    def __init__(self, image, canny_th1, canny_th2):
        self.image = None
        super().__init__(image)
        try:
            if isinstance(canny_th1, int):
                if isinstance(canny_th2, int):
                    self.image = cv.Canny(self.image, canny_th1, canny_th2)
                else:
                    raise ValueError(
                        f"Input variable 'canny_th2' can just be int.")
            else:
                raise ValueError(
                    f"Input variable 'canny_th1' can just be int.")
        except Exception as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    pass
