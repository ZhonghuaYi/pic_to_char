# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-08

from Pic import *


class Video:
    def __init__(self, video_path):
        self._video_path = video_path
        self._video = cv.VideoCapture(self._video_path)
        self._frame_count = self._video.get(cv.CAP_PROP_FRAME_COUNT)
        self._fps = self._video.get(cv.CAP_PROP_FPS)
        self._frames = self._load()

    def __getattribute__(self, item):
        """ Auto run when use object's attribute.

        If attribute is None, will occur an exception.

        Args:
            item: str.

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

    @property
    def video_path(self):
        return self._video_path

    @property
    def video(self):
        return self._video

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def fps(self):
        return self._fps

    @property
    def frames(self):
        return self._frames

    def _load(self):
        v = self.video
        ret, frame = v.read()
        try:
            while ret:
                pic = Pic(frame)
                pic.resize((240, 180))
                yield pic
                ret, frame = v.read()
        except Exception as e:
            print(e)
            sys.exit()

    def reload(self):
        self._frames = self._load()

    def play(self, speed=1.):
        frames = self.frames
        frame_delay = int(1000 / (self.fps * speed))
        window_name = self.video_path
        for frame in frames:
            cv.imshow(window_name, frame.image)
            if cv.waitKey(frame_delay) == ord('q'):
                break


class CharVideo(Video):
    def __init__(self, video_path):
        self._char_frames = None
        super().__init__(video_path)

    @property
    def char_frames(self):
        return self._char_frames

    def generate_char_frames(self, font_path, font_size, charset=None, color=(255, 255, 255)):
        frames = self.frames

        def char_frame_iter():
            for frame in frames:
                char_pic = CharPic(frame)
                char_pic.generate_matrix_and_image(font_path, font_size, charset, color)
                yield char_pic

        self._char_frames = char_frame_iter()

    def save_char_video(self, save_path, codec, fps, frame_size=(0, 0)):
        new_size = list(frame_size)
        char_frames = self.char_frames
        char_frame = char_frames.__next__()
        if frame_size[0] == 0:
            new_size[0] = char_frame.char_image.shape[1]
        if frame_size[1] == 0:
            new_size[1] = char_frame.char_image.shape[0]
        fourcc = cv.VideoWriter_fourcc(*codec)
        writer = cv.VideoWriter(save_path, fourcc, fps, new_size)
        writer.write(char_frame.char_image)
        for char_frame in char_frames:
            writer.write(char_frame.char_image)
        print("Video saved.")


if __name__ == '__main__':
    font_path = "C:/Windows/Fonts/Monaco.ttf"
    path = "./test.mp4"
    v = CharVideo(path)
    # for i in range(100):
    #     v.frames.__next__()
    # i = CharPic(v.frames.__next__())
    # i.generate_matrix_and_image(font_path, 3)
    # i.show(image_type="char_image")
    v.generate_char_frames(font_path, 3)
    v.save_char_video("./1.mp4", "mp4v", v.fps)
