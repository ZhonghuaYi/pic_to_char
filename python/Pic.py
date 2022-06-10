# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09

import sys
import numpy as np
import cv2 as cv
from PIL import Image


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
            item:

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
        cv.imshow(window_name, self.image)
        cv.waitKey(delay)

    def resize(self, size=(0, 0), fx=1., fy=1.):
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


if __name__ == '__main__':
    path = "./test.jpg"
    i = Pic(path)
    print(i.c)