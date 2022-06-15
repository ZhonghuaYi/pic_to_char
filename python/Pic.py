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
            fx (float, optional): Horizental stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        new_size = list(size)
        if size[0] == 0:
            new_size[0] = self._image.shape[1]
        if size[1] == 0:
            new_size[1] = self._image.shape[0]
        self._image = cv.resize(self._image, dsize=new_size)
        if fx == 1 and fy == 1:
            return
        else:
            self._image = cv.resize(self._image, (0, 0), fx=fx, fy=fy)
        return


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
            elif method == 1:
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
            fx (float, optional): Horizental stretching ratio. Defaults to 1..
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


class CharPic(GrayPic):
    def __init__(self, image):
        """
        Initialize CharPic object.
        Args:
            image: str or numpy.ndarray or Pic or PIL.Image.Image.
        """
        self._image = None
        self._char_matrix = None
        self._char_image = None
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"
        super().__init__(image)

    @property
    def char_matrix(self):
        return self._char_matrix

    @property
    def char_image(self):
        return self._char_image

    @property
    def charset(self):
        return self.__charSet

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
        gray = self.image
        char_matrix = charset[(gray / (256 / charset.size)).astype(
            np.int32)]
        self._char_matrix = char_matrix
        return char_matrix

    def save_char_matrix(self, file_path):
        """Save char matrix to file.

        Args:
            file_path (str): File path to save char matrix.
        """
        np.savetxt(file_path, self._char_matrix, fmt="%s")

    def generate_char_image(self, font_path=None, font_size=5, color=(255, 255, 255)):
        """Generate char image from char matrix.

        Args:
            font_path (str): Path to font file.
            font_size (int): Font size.
            color (tuple, optional): Font color. Defaults to (255, 255, 255).

        Returns:
            ndarray: char image.
        """
        matrix_shape = self._char_matrix.shape
        if font_path is None:
            canvas_size = (matrix_shape[1] * 7, matrix_shape[0] * 7)
            canvas = np.zeros(canvas_size, dtype=np.uint8)
            for i in range(matrix_shape[0]):
                for j in range(matrix_shape[1]):
                    cv.putText(canvas, self._char_matrix[i, j], (j * 7, i * 7), 1, 0.5, color)
        else:
            font = ImageFont.truetype(font_path, font_size)
            canvas_size = (matrix_shape[1] * font_size,
                           matrix_shape[0] * font_size)
            canvas = Image.new("RGB", canvas_size)
            canvas_draw = ImageDraw.Draw(canvas)
            for i in range(matrix_shape[0]):
                for j in range(matrix_shape[1]):
                    canvas_draw.text((j * font_size, i * font_size),
                                     self._char_matrix[i][j],
                                     font=font,
                                     fill=color)
            canvas = cv.cvtColor(np.asarray(canvas), cv.COLOR_RGB2BGR)
        # cv.imshow("char_image", canvas)
        # cv.waitKey(0)
        self._char_image = canvas
        return self._char_image

    def generate_matrix_and_image(self, font_path=None, font_size=5, charset=None, color=(255, 255, 255)):
        self.generate_char_matrix(charset)
        self.generate_char_image(font_path, font_size, color)

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
        image_type = "_" + image_type
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
    import time
    t1 = time.time()
    font_path = "./Monaco.ttf"
    path = "./test.jpg"
    image = CharPic(path)
    image.resize(size=(300, 300))
    image.generate_matrix_and_image()
    t2 = time.time()
    print(t2-t1)
    image.show('', image_type="char_image")
