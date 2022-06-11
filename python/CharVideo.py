# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-08

from Pic import *

class Video:
    def __init__(self, video_path):
        self._video = cv.VideoCapture(video_path)
        self._frame_count = self._video.get(cv.CAP_PROP_FRAME_COUNT)
        self._fps = self._video.get(cv.CAP_PROP_FPS)

    def play(self, speed=1.):
        v = self._video
        count = 0



if __name__ == '__main__':
    pass
