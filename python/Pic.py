# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09

import sys
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
        self.image = None
        if isinstance(image, str):
            self.image = cv.imread(image, 1)
        elif isinstance(image, np.ndarray):
            self.image = image
        elif isinstance(image, Pic):
            self.image = image.image
        elif isinstance(image, Image.Image):
            i = np.asarray(image)
            if i.ndim == 3:
                self.image = cv.cvtColor(i, cv.COLOR_RGB2BGR)
            elif i.ndim == 2:
                self.image = i
        try:
            if self.__dict__["image"] is None:
                raise AttributeError("Reading image failed.")
        except Exception as e:
            print(e)
            sys.exit()

    def __getattribute__(self, item):
        """ Auto run when use object's attribute.

        If attribute is None, will occur an exception.

        Args:
            item: str.

        Returns:

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

    def show(self, window_name='', delay=0):
        """ Show image.

        Args:
            window_name (str, optional): Window's name. Defaults to ''.
            delay (int, optional): Time that window delay. Defaults to 0.
        """
        cv.imshow(window_name, self.image)
        cv.waitKey(delay)

    def resize(self, size=(0, 0), fx=1., fy=1.):
        """ Resize image.

        Args:
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizental stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        new_size = list(size)
        if size[0] == 0:
            new_size[0] = self.image.shape[1]
        if size[1] == 0:
            new_size[1] = self.image.shape[0]
        self.image = cv.resize(self.image, dsize=new_size)
        if fx == 1 and fy == 1:
            return
        else:
            self.image = cv.resize(self.image, (0, 0), fx=fx, fy=fy)
        return


class ColorPic(Pic):
    def __init__(self, image):
        """Make sure self.image is a 3-d ndarray object."""
        self.image = None
        super().__init__(image)
        if self.image.ndim == 2:
            self.image = cv.cvtColor(self.image, cv.COLOR_GRAY2BGR)


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
        """ Resize image. And make sure result is a binary image.

        Args:
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizental stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
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
        """Initialize EdgePic object.

        Args:
            image: str or numpy.ndarray or Pic or PIL.Image.Image.
            canny_th1: int. Canny threshold 1.
            canny_th2: int. Canny threshold 2.
        """
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


class CharPic(Pic):
    def __init__(self, image):
        """
        Initialize CharPic object.
        Args:
            image: str or numpy.ndarray or Pic or PIL.Image.Image.
        """
        self.image = None
        self.char_matrix = None
        self.char_image = None
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"
        super().__init__(image)

    def generate_char_matrix(self, charset=None):
        """
        Generate char matrix from image.
        Args:
            charset (str, optional): Char set to represent grayscale from 0 to 255.
                                         Defaults to None.
        Returns:
            ndarray: char matrix.
        """
        if charset is None:
            charset = self.__charSet
        charset = np.asarray(list(charset), dtype=str)
        gray = GrayPic(self.image)
        char_matrix = charset[(gray.image / (256 / charset.size)).astype(
            np.int32)]
        self.char_matrix = char_matrix
        return char_matrix

    def save_char_matrix(self, file_path):
        """Save char matrix to file.

        Args:
            file_path (str): File path to save char matrix.
        """
        np.savetxt(file_path, self.char_matrix, fmt="%s")

    def generate_char_image(self, font_path, font_size, color=(255, 255, 255)):
        """Generate char image from char matrix.

        Args:
            font_path (str): Path to font file.
            font_size (int): Font size.
            color (tuple, optional): Font color. Defaults to (255, 255, 255).

        Returns:
            ndarray: char image.
        """
        matrix_shape = self.char_matrix.shape
        font = ImageFont.truetype(font_path, font_size)
        canvas_size = (matrix_shape[1] * font_size,
                       matrix_shape[0] * font_size)
        canvas = Image.new("RGB", canvas_size)
        canvas_draw = ImageDraw.Draw(canvas)
        for i in range(matrix_shape[0]):
            for j in range(matrix_shape[1]):
                canvas_draw.text((j * font_size, i * font_size),
                                 self.char_matrix[i][j],
                                 font=font,
                                 fill=color)
        char_image = cv.cvtColor(np.asarray(canvas), cv.COLOR_RGB2BGR)
        self.char_image = char_image
        return self.char_image

    def show(self, window_name='', image_type="image", delay=0):
        """Show image.

        Args:
            window_name (str, optional): Window's name. Defaults to ''.
            image_type (str, optional): Image type. Defaults to "image".
            delay (int, optional): Time that window delay. Defaults to 0.
        """
        image = self.__getattribute__(image_type)
        cv.imshow(window_name, image)
        cv.waitKey(delay)
        sys.exit()

    def resize(self, image_type="image", size=(0, 0), fx=1., fy=1.):
        """Resize image.

        Args:
            image_type (str, optional): Image type. Defaults to "image".
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizental stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        new_size = list(size)
        image = self.__getattribute__(image_type)
        if size[0] == 0:
            new_size[0] = image.shape[1]
        if size[1] == 0:
            new_size[1] = image.shape[0]
        self.__dict__[image_type] = cv.resize(image, dsize=new_size)
        if fx == 1 and fy == 1:
            return
        else:
            self.__dict__[image_type] = cv.resize(image, (0, 0), fx=fx, fy=fy)
        return


if __name__ == '__main__':
    pass
