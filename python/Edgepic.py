# -*- coding: utf-8 -*- 
# @Author:  ZhonghuaYi
# @Time  :  2022-06-09

import Pic
from PicProcess import PicProcess


class EdgePic(Pic.GrayPic):
    def __init__(self, image, canny_th1, canny_th2):
        self.image = None
        super().__init__(image)
        self.image = PicProcess.gray_to_edge(Pic.GrayPic(image), canny_th1, canny_th2)


if __name__ == '__main__':
    image = "./test.jpg"
    a = Pic.GrayPic(image)
    a.resize((200, 200))
    i = EdgePic(a, 20, 80)
    print(a.image.shape)
    print(i.image.shape)
    i.show()
