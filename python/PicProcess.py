# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09
import sys

import cv2 as cv


class PicProcess:
    @staticmethod
    def image_to_gray(image, color_space="BGR"):
        dim = image.ndim
        try:
            if dim == 2:
                image = image
            elif dim == 3:
                if color_space == "BGR":
                    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                elif color_space == "RGB":
                    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
                else:
                    bgr_image = image
                    if color_space == "HSV":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_HSV2BGR)
                    elif color_space == "XYZ":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_XYZ2BGR)
                    elif color_space == "HLS":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_HLS2BGR)
                    elif color_space == "LAB" or color_space == "Lab":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_LAB2BGR)
                    elif color_space == "LUV" or color_space == "Luv":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_LUV2BGR)
                    elif color_space == "YUV":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_YUV2BGR)
                    elif color_space == "YCrCb":
                        bgr_image = cv.cvtColor(bgr_image, cv.COLOR_YCrCb2BGR)
                    else:
                        raise ValueError(
                            f"Color space {color_space} not supported.")
                    image = cv.cvtColor(bgr_image, cv.COLOR_BGR2GRAY)
            elif dim == 4:
                if color_space == "BGRA":
                    image = cv.cvtColor(image, cv.COLOR_BGRA2GRAY)
                elif color_space == "RGBA":
                    image = cv.cvtColor(image, cv.COLOR_RGBA2GRAY)
                else:
                    raise ValueError(
                        f"Color space {color_space} not supported.")
            else:
                raise ValueError(
                    "Image's dimension not supported. Only support 2, 3 and 4."
                )
        except Exception as e:
            print(e)
            sys.exit()
        return image


if __name__ == '__main__':
    pass
