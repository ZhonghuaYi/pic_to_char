# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-07
"""
The entry of the project.
"""

from CharPic import *
from Pic import *
from ColorPic import *
from GrayPic import *

if __name__ == '__main__':
    image = "./test.jpg"
    font_path = "C:/Windows/Fonts/Monaco.ttf"
    image = CharPic(1)
    image.show()
