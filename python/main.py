# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-07
"""
The entry of the project.
"""

from Pic import *

if __name__ == '__main__':
    image = "./test.jpg"
    font_path = "./Monaco.ttf"
    image = CharPic(image)
    print(dir(image))
