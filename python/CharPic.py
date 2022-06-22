# -*- coding: utf-8 -*- 
# @Author:  ZhonghuaYi
# @Time  :  2022-06-21

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from Pic import *
from PicProcess import PicProcess


class CharPic(Pic):
    def __init__(self, image):
        """
        Initialize CharPic object.
        """
        self._char_matrix = None
        self.__image_flag = 0
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"
        super().__init__(image)

    def __getattribute__(self, item):
        """ Auto run when use object's attribute.

        If attribute is None, will occur an exception.

        Args:
            item: str.

        Returns: item attribute

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
    def char_matrix(self):
        return self._char_matrix

    @property
    def image_flag(self):
        return self.__image_flag

    @property
    def charset(self):
        return self.__charSet

    def generate_char_matrix(self, charset=None):
        """
        Generate char matrix from image.
        Args:
            charset (str, optional): Char set to represent grayscale from 0 to 255.
                                         Defaults to None.
        Returns:
            ndarray: char matrix.
        """
        gray = PicProcess.image_to_gray(self.image)
        if charset is None:
            charset = self.__charSet
        charset = np.asarray(list(charset), dtype=str)
        char_matrix = charset[(gray / (256 / charset.size)).astype(np.int32)]
        self._char_matrix = char_matrix
        return char_matrix

    def save_char_matrix(self, file_path):
        """Save char matrix to file.

        Args:
            file_path (str): File path to save char matrix.
        """
        np.savetxt(file_path, self._char_matrix, fmt="%s")

    def load_char_matrix(self, file_path):
        """Load char matrix from file.

        Args:
            file_path (str): File path to save char matrix.
        """
        np.loadtxt(file_path, self._char_matrix, fmt="%s")

    def generate_char_image(self,
                            font_path=None,
                            font_size=5,
                            background=(0, 0, 0),
                            color=(255, 255, 255)):
        """Generate char image from char matrix.

        Args:
            background (tuple, optional): Background color. Defaults to (255, 255, 255).
            font_path (str): Path to font file.
            font_size (int): Font size.
            color (tuple, optional): Font color. Defaults to (255, 255, 255).

        Returns:
            ndarray: char image.
        """
        matrix_shape = self._char_matrix.shape
        if font_path is None:
            use_thread = False
            if use_thread:
                threads = []
                sub_rows = matrix_shape[0] // 5
                for i in range(5):
                    threads.append(
                        CharThread(
                            self._char_matrix[i * sub_rows:(i + 1) * sub_rows, :],
                            color))
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                canvas = np.zeros((matrix_shape[0] * 7, matrix_shape[1] * 7, 3),
                                  dtype=np.uint8)
                for i in range(5):
                    canvas[i * sub_rows * 7:(i + 1) * sub_rows * 7, :, :] = threads[
                        i].get_canvas()
            else:
                canvas_size = (matrix_shape[0] * 7, matrix_shape[1] * 7, 3)
                canvas = np.ones(canvas_size, dtype=np.uint8)
                for i in range(3):
                    canvas[:, :, i] = canvas[:, :, i] * background[i]
                for i in range(matrix_shape[0]):
                    for j in range(matrix_shape[1]):
                        cv.putText(canvas, self._char_matrix[i, j], (j * 7, i * 7),
                                   1, 0.5, color)
        else:
            font = ImageFont.truetype(font_path, font_size)
            canvas_size = (matrix_shape[1] * font_size,
                           matrix_shape[0] * font_size)
            canvas = Image.new("RGB", canvas_size)
            canvas_draw = ImageDraw.Draw(canvas)
            for i in range(matrix_shape[0]):
                for j in range(matrix_shape[1]):
                    canvas_draw.text((j * font_size, i * font_size),
                                     self._char_matrix[i][j],
                                     font=font,
                                     fill=color)
            canvas = cv.cvtColor(np.asarray(canvas), cv.COLOR_RGB2BGR)
        self._image = canvas
        self.__image_flag += 1
        return self._image

    def generate_matrix_and_image(self,
                                  font_path=None,
                                  font_size=5,
                                  charset=None,
                                  background=(0, 0, 0),
                                  color=(255, 255, 255)):
        self.generate_char_matrix(charset)
        self.generate_char_image(font_path, font_size, background, color)


if __name__ == '__main__':
    import time
    t1 = time.time()
    font_path = "./Monaco.ttf"
    path = "./test.jpg"
    image = CharPic(path)
    image.resize((200, 200))
    image.generate_matrix_and_image(background=(255, 0, 0))
    t2 = time.time()
    print(t2 - t1)
    image.show()
