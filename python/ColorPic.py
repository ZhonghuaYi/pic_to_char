# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-10

from Pic import Pic
import cv2 as cv


class ColorPic(Pic):
    def __init__(self, image):
        """Make sure self.image is a 3-d ndarray object."""
        self.image = None
        super().__init__(image)
        if self.image.ndim == 2:
            self.image = cv.cvtColor(self.image, cv.COLOR_GRAY2BGR)


if __name__ == '__main__':
    pass
