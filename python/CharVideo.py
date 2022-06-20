# -*- coding: utf-8 -*-
# @Author:  ZhonghuaYi
# @Time  :  2022-06-08

from CharPic import *


class Video:
    def __init__(self, video_path, new_size=None, fx=1., fy=1.):
        self._video_path = video_path
        self._video = cv.VideoCapture(self._video_path)
        self._frame_count = self._video.get(cv.CAP_PROP_FRAME_COUNT)
        self._fps = self._video.get(cv.CAP_PROP_FPS)
        self._frames = self._load(new_size, fx, fy)

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

    def _load(self, new_size=None, fx=1., fy=1.):
        v = self.video
        ret, frame = v.read()
        try:
            while ret:
                pic = Pic(frame)
                if new_size is not None:
                    pic.resize(new_size, fx, fy)
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

    def generate_char_frames(self, font_path=None, font_size=5, charset=None, color=(255, 255, 255)):
        frames = self.frames

        def char_frame_iter():
            for frame in frames:
                char_pic = CharPic()
                char_pic.generate_matrix_and_image(frame.image, font_path, font_size, charset, color)
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

    def play(self, video_type="frames", speed=1.):
        try:
            frames = None
            if video_type == "frames":
                frames = self.frames
            elif video_type == "char_frames":
                frames = self.char_frames
            else:
                raise ValueError(f"Video type '{video_type}' is not supported.")
            frame_delay = int(1000 / (self.fps * speed))
            window_name = self.video_path
            for frame in frames:
                if video_type == "frames":
                    cv.imshow(window_name, frame.image)
                elif video_type == "char_frames":
                    cv.imshow(window_name, frame.char_image)
                if cv.waitKey(frame_delay) == ord('q'):
                    break
        except Exception as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    import time
    time_start = time.time()
    font_path = "./Monaco.ttf"
    path = "./test.mp4"
    v = CharVideo(path)
    v.generate_char_frames()
    v.save_char_video("./1.mp4", "mp4v", v.fps)
    time_end = time.time()
    print(f"Time used: {time_end - time_start}")
