# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09

import sys
import threading
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont

from PicProcess import PicProcess


class Pic:
    def __init__(self, image):
        """ Initialize new object.

        Args:
            image: str or numpy.ndarray or Pic or PIL.Image.Image.
        """
        self._image = None
        if isinstance(image, str):
            self._image = cv.imread(image, 1)
        elif isinstance(image, np.ndarray):
            self._image = image
        elif isinstance(image, Pic):
            self._image = image.image
        elif isinstance(image, Image.Image):
            i = np.asarray(image)
            if i.ndim == 3:
                self._image = cv.cvtColor(i, cv.COLOR_RGB2BGR)
            elif i.ndim == 2:
                self._image = i
        try:
            if self.__dict__["_image"] is None:
                raise AttributeError("Reading image failed.")
        except Exception as e:
            print(e)
            sys.exit()

    def __getattribute__(self, item):
        """ Auto run when use object's attribute.

        If attribute is None, will occur an exception.

        Args:
            item: str.

        Returns: item attribute

        """
        item_value = super().__getattribute__(item)
        try:
            if item_value is None:
                raise TypeError(f"Object attribute '{item}' of class "
                                f"'{self.__class__.__name__}' is None")
        except Exception as e:
            print(e)
            sys.exit()
        return item_value

    @property
    def image(self):
        return self._image

    def show(self, window_name='', delay=0):
        """ Show image.

        Args:
            window_name (str, optional): Window's name. Defaults to ''.
            delay (int, optional): Time that window delay. Defaults to 0.
        """
        cv.imshow(window_name, self._image)
        cv.waitKey(delay)

    def resize(self, size=(0, 0), fx=1., fy=1.):
        """ Resize image.

        Args:
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizontal stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        image = self.__getattribute__("_image")
        self._image = PicProcess.image_resize(image, size, fx, fy)

    def save_image(self, file_path):
        """ Save image.

        Args:
            file_path (str): File path.
        """
        image = self.__getattribute__("_image")
        cv.imwrite(file_path, image)


class ColorPic(Pic):
    def __init__(self, image):
        """Make sure self._image is a 3-d ndarray object."""
        self._image = None
        super().__init__(image)
        if self._image.ndim == 2:
            self._image = cv.cvtColor(self._image, cv.COLOR_GRAY2BGR)


class GrayPic(Pic):
    def __init__(self, image):
        """Make sure self._image is a 2-d ndarray object."""
        self._image = None
        super().__init__(image)
        self._image = PicProcess.image_to_gray(self._image)


class BinaryPic(GrayPic):
    def __init__(self, image, method=0, thresh=-1):
        self._image = None
        self._th = None
        super().__init__(image)
        try:
            if method == 0:
                self._th, self._image = cv.threshold(
                    self._image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            elif method == 1:
                if thresh <= 0 or thresh >= 255:
                    raise ValueError(
                        f"Wrong input variable: 'thresh'={thresh}")
                self._th, self._image = cv.threshold(self._image, thresh, 255,
                                                     cv.THRESH_BINARY)
            elif method == 2:
                self._image = cv.adaptiveThreshold(self.gray, 255,
                                                   cv.ADAPTIVE_THRESH_MEAN_C,
                                                   cv.THRESH_BINARY, 5, 0)
                self._th = -1
            else:
                raise ValueError(f"Wrong input variable: 'method'={method}")
        except Exception as e:
            print(e)
            sys.exit()

    @property
    def th(self):
        return self._th

    def resize(self, size=(0, 0), fx=1., fy=1.):
        """ Resize image. And make sure result is a binary image.

        Args:
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizontal stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        super().resize(size=size, fx=fx, fy=fy)
        if 0 < self._th < 255:
            _, self._image = cv.threshold(self._image, self._th, 255,
                                          cv.THRESH_BINARY)
        elif self._th == -1:
            self._image = cv.adaptiveThreshold(self.gray, 255,
                                               cv.ADAPTIVE_THRESH_MEAN_C,
                                               cv.THRESH_BINARY, 5, 0)


class EdgePic(BinaryPic):
    def __init__(self, image, canny_th1, canny_th2):
        """Initialize EdgePic object.

        Args:
            image: str or numpy.ndarray or Pic or PIL.Image.Image.
            canny_th1: int. Canny threshold 1.
            canny_th2: int. Canny threshold 2.
        """
        self._image = None
        super().__init__(image)
        try:
            if isinstance(canny_th1, int):
                if isinstance(canny_th2, int):
                    self._image = cv.Canny(self._image, canny_th1, canny_th2)
                else:
                    raise ValueError(
                        f"Input variable 'canny_th2' can just be int.")
            else:
                raise ValueError(
                    f"Input variable 'canny_th1' can just be int.")
        except Exception as e:
            print(e)
            sys.exit()


class CharThread(threading.Thread):
    def __init__(self, char_matrix, color):
        super().__init__()
        self._canvas = None
        self._char_matrix = char_matrix
        self._matrix_shape = char_matrix.shape
        self._color = color

    def run(self):
        canvas_size = (self._matrix_shape[0] * 7, self._matrix_shape[1] * 7)
        canvas = np.zeros(canvas_size, dtype=np.uint8)
        for i in range(self._matrix_shape[0]):
            for j in range(self._matrix_shape[1]):
                cv.putText(canvas, self._char_matrix[i, j], (j * 7, i * 7), 1,
                           0.5, self._color)
        canvas = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)
        self._canvas = canvas

    def get_canvas(self):
        return self._canvas


if __name__ == '__main__':
    pass
