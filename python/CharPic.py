# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-07
import sys

import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from Pic import Pic
from GrayPic import GrayPic


class CharPic(Pic):
    """
    Class used to generate char image.
    Args:
        Pic : Base class of image.
    """
    def __init__(self, image):
        """
        Initialize CharPic object.
        Args:
            image: Image path.
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
        np.savetxt(file_path, self.char_matrix, fmt="%s")

    def generate_char_image(self, font_path, font_size, color=(255, 255, 255)):
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
        image = self.__getattribute__(image_type)
        cv.imshow(window_name, image)
        cv.waitKey(delay)
        sys.exit()

    def resize(self, image_type="image", size=(0, 0), fx=1., fy=1.):
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
