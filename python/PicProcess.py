# -*- coding: utf-8 -*- 
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09

import sys
import Pic
import cv2 as cv


class PicProcess:
    @staticmethod
    def gray_to_edge(gray, canny_th1, canny_th2):
        try:
            if not isinstance(gray, Pic.GrayPic):
                raise TypeError("Parameter 'gray' is not an instance of class GrayPic")
            gray_img = gray.image
            edge_img = cv.Canny(gray_img, canny_th1, canny_th2)
            return edge_img
        except Exception as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    pass
