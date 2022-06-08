# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-07

import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw


class Pic:
    """
    Base class of image.
    """
    def __init__(self, image_path):
        self.binary_th = None
        self.edge = None
        self.binary = None
        self.image = cv.imread(image_path, 1)
        self.gray = cv.imread(image_path, 0)

    def show(self, image_type="image", window_name="Pic", delay=0):
        """
        Show image of given type.

        Args:
            image_type (string, optional): "binary" or "edge" or "gray" or"image". Defaults to "image".
            window_name (string, optional): Name of displayed window. Defaults to "Pic".
            delay (int, optional): Time(ms) that window delay. Defaults to 0.
        """
        try:
            if image_type == "binary":
                if self.binary is None:
                    raise TypeError("Object attribute 'binary' is None.")
                image = self.binary
            elif image_type == "edge":
                if self.edge is None:
                    raise TypeError("Object attribute 'edge' is None.")
                image = self.edge
            elif image_type == "gray":
                image = self.gray
            else:
                image = self.image

            cv.imshow(window_name, image)
            cv.waitKey(delay)
        except TypeError as te:
            print(te)

    def to_binary(self, method=2, thresh=-1):
        """
        Greneate binary image.

        Args:
            method (int, optional): Choose threhold method. Defaults to 2.
            thresh (int, optional): Input threshold when threshold method needs. Defaults to -1.

        Returns:
            ndarray: Binary image.
        """
        try:
            if method == 0:
                self.binary = cv.adaptiveThreshold(self.gray, 255,
                                                   cv.ADAPTIVE_THRESH_MEAN_C,
                                                   cv.THRESH_BINARY, 5, 0)
                self.binary_th = -1
            if method == 1:
                if thresh <= 0 or thresh >= 255:
                    raise ValueError(f"Wrong input variable: thresh={thresh}")
                self.binary_th, self.binary = cv.threshold(
                    self.gray, thresh, 255, cv.THRESH_BINARY)
            if method == 2:
                self.binary_th, self.binary = cv.threshold(
                    self.gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        except ValueError as ve:
            print(ve)
        return self.binary

    def to_edge(self, thresh1, thresh2, use_binary=False):
        """
        Use Canny to generate edge image.

        Args:
            thresh1 (int): Threshold1 for Canny.
            thresh2 (int): Threshold2 for Canny.
            use_binary (bool, optional): Use binary or gray image. Defaults to False.

        Returns:
            ndarray: Edge image.
        """
        try:
            if use_binary:
                if self.binary is None:
                    raise TypeError("Object attribute 'binary' is None.")
                self.edge = cv.Canny(self.binary, thresh1, thresh2)
            else:
                self.edge = cv.Canny(self.gray, thresh1, thresh2)
        except TypeError as te:
            print(te)
        return self.edge

    def to_binary_and_edge(self,
                           canny_thresh1,
                           canny_thresh2,
                           binary_method=2,
                           binary_thresh=-1):
        """
        Generate binary image and edge image once.

        Args:
            canny_thresh1 (int): Threshold1 for Canny.
            canny_thresh2 (int): Threshold2 for Canny.
            binary_method (int, optional): Choose threhold method. Defaults to 2.
            binary_thresh (int, optional): Input threshold when threshold method needs. Defaults to -1.

        Returns:
            (ndarray, ndarray): Binary image and edge image.
        """
        self.to_binary(binary_method, binary_thresh)
        self.to_edge(canny_thresh1, canny_thresh2)
        return self.binary, self.edge

    def resize(self, size=None):
        """
        Reisze all the images of the object.

        Args:
            size (tuple, optional): (width, height) of the new image. Defaults to None.
        """
        if size is not None:
            self.image = cv.resize(self.image, size)
            self.gray = cv.resize(self.gray, size)
            if self.binary is not None:
                self.binary = cv.resize(self.binary, size)
            if self.edge is not None:
                self.edge = cv.resize(self.edge, size)


class CharPic(Pic):
    """
    Class used to generate char image.

    Args:
        Pic : Base class of image.
    """
    def __init__(self, image_path):
        """
        Initialize CharPic object.

        Args:
            image_path (string): Image path.
        """
        super().__init__(image_path)
        self.char_matrix = None
        self.char_image = None
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"

    def to_char(self, image=None, charset=None):
        """
        Generate char matrix from image.

        Args:
            image (ndarray, optional): Where char matrix is from. Defaults to None.
            charset (string, optional): Char set to represent grayscale from 0 to 255. 
                                         Defaults to None.

        Returns:
            ndarray: char matrix.
        """
        if image is None:
            image = self.gray
        if charset is None:
            charset = self.__charSet
        charset = np.asarray(list(charset), dtype=str)
        char_matrix = charset[(image / (256 / charset.size)).astype(np.int32)]
        self.char_matrix = char_matrix
        return char_matrix

    def gray_to_char(self, charset=None):
        """
        Generate char matrix from gray image.

        Args:
            charset (string, optional): Char set to represent grayscale from 0 to 255. 
                                        Defaults to None.

        Returns:
            ndarray: char matrix.
        """
        return self.to_char(self.gray, charset)

    def binary_to_char(self, charset=None):
        """
        Generate char matrix from binary image.

        Args:
            charset (string, optional): Char set to represent grayscale from 0 to 255. 
                                        Defaults to None.

        Returns:
            ndarray: char matrix.
        """
        return self.to_char(self.binary, charset)

    def edge_to_char(self, charset=None):
        """
        Generate char matrix from edge image.

        Args:
            charset (string, optional): Char set to represent grayscale from 0 to 255. 
                                        Defaults to None.

        Returns:
            ndarray: char matrix.
        """
        return self.to_char(self.edge, charset)
    
    def generate_char_image(self):
        try:
            if self.char_matrix is None:
                raise TypeError("Object attribute 'char_matrix' is None.")
            
        except TypeError as te:
            print(te)

    def save_char_matrix(self, file_path):
        np.savetxt(file_path, self.char_matrix, fmt="%s")


if __name__ == '__main__':
    image = "./test.jpg"
    i = Pic(image)
    i.resize((200, 300))
    i.to_binary_and_edge(100, 200)
