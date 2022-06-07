# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-07

import cv2 as cv
import numpy as np


class Pic:
    def __init__(self, image_path):
        self.binary_th = None
        self.edge = None
        self.binary = None
        self.image = cv.imread(image_path, 0)

    def show(self, image_type=None, window_name=None, delay=0):
        try:
            if image_type == "binary":
                if self.binary is None:
                    raise TypeError("Object attribute 'binary' is None.")
                image = self.binary
            elif image_type == "edge":
                if self.edge is None:
                    raise TypeError("Object attribute 'edge' is None.")
                image = self.edge
            else:
                image = self.image
            if not window_name:
                cv.imshow("Pic", image)
            else:
                cv.imshow(window_name, image)
            cv.waitKey(delay)
        except TypeError as te:
            print(te)

    def to_binary(self, method=0, thresh=-1):
        try:
            if method == 0:
                self.binary = cv.adaptiveThreshold(self.image, 255,
                                                   cv.ADAPTIVE_THRESH_MEAN_C,
                                                   cv.THRESH_BINARY, 5, 0)
                self.binary_th = -1
            if method == 1:
                if thresh <= 0 or thresh >= 255:
                    raise ValueError(f"Wrong input variable: thresh={thresh}")
                self.binary_th, self.binary = cv.threshold(self.image, thresh, 255,
                                              cv.THRESH_BINARY)
            if method == 2:
                self.binary_th, self.binary = cv.threshold(
                    self.image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        except ValueError as ve:
            print(ve)
        return self.binary

    def to_edge(self, thresh1, thresh2, use_binary=False):
        try:
            if use_binary:
                if self.binary is None:
                    raise TypeError("Object attribute 'binary' is None.")
                self.edge = cv.Canny(self.binary, thresh1, thresh2)
            else:
                self.edge = cv.Canny(self.image, thresh1, thresh2)
        except TypeError as te:
            print(te)
        return self.edge

    def to_binary_and_edge(self,
                           canny_thresh1,
                           canny_thresh2,
                           binary_method=0,
                           binary_thresh=-1):
        self.to_binary(binary_method, binary_thresh)
        self.to_edge(canny_thresh1, canny_thresh2)
        return self.binary, self.edge


class CharPic(Pic):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"

    def binary_to_char(self, char_set=None):
        if char_set is None:
            char_set = self.__charSet
        # char_matrix = np.zeros(shape=self.binary.shape, dtype=str)
        binary = self.binary
        char_matrix = (binary / len(char_set)).astype(np.int32)
        print(char_matrix)


if __name__ == '__main__':
    image = "./test.jpg"
    p = CharPic(image)
    p.to_binary(2)
    print(p.binary_th)
    cv.imshow("binary", p.binary)
    cv.waitKey(0)
