# -*- coding: utf-8 -*- 
# @Author:  ZhonghuaYi
# @Time  :  2022-06-21

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from Pic import *
from PicProcess import PicProcess


class CharPic:
    def __init__(self):
        """
        Initialize CharPic object.
        """
        self._char_matrix = None
        self._char_image = None
        self.__charSet = ".\'`^\",:Il!i><~+_-?]}1)|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$"

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
    def char_image(self):
        return self._char_image

    @property
    def charset(self):
        return self.__charSet

    def generate_char_matrix(self, gray, charset=None):
        """
        Generate char matrix from image.
        Args:
            gray: 2-d ndarray.
            charset (str, optional): Char set to represent grayscale from 0 to 255.
                                         Defaults to None.
        Returns:
            ndarray: char matrix.
        """
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
                            color=(255, 255, 255)):
        """Generate char image from char matrix.

        Args:
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
                canvas_size = (matrix_shape[0] * 7, matrix_shape[1] * 7)
                canvas = np.zeros(canvas_size, dtype=np.uint8)
                for i in range(matrix_shape[0]):
                    for j in range(matrix_shape[1]):
                        cv.putText(canvas, self._char_matrix[i, j], (j * 7, i * 7),
                                   1, 0.5, color)
                canvas = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)
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
        # cv.imshow("char_image", canvas)
        # cv.waitKey(0)
        self._char_image = canvas
        return self._char_image

    def generate_matrix_and_image(self,
                                  gray,
                                  font_path=None,
                                  font_size=5,
                                  charset=None,
                                  color=(255, 255, 255)):
        self.generate_char_matrix(gray, charset)
        self.generate_char_image(font_path, font_size, color)

    def show(self, window_name='', delay=0):
        """Show image.

        Args:
            window_name (str, optional): Window's name. Defaults to ''.
            delay (int, optional): Time that window delay. Defaults to 0.
        """
        image = self.__getattribute__("char_image")
        cv.imshow(window_name, image)
        cv.waitKey(delay)
        sys.exit()

    def resize(self, size=(0, 0), fx=1., fy=1.):
        """Resize image.

        Args:
            size (tuple, optional): New size of image. Defaults to (0, 0).
            fx (float, optional): Horizontal stretching ratio. Defaults to 1..
            fy (float, optional): Vertical stretching ratio. Defaults to 1..
        """
        image = self.__getattribute__("_char_image")
        self._char_image = PicProcess.image_resize(image, size, fx, fy)

    def save_image(self, file_path):
        """ Save image.

        Args:
            file_path (str): File path.
        """
        image = self.__getattribute__("_char_image")
        cv.imwrite(file_path, image)


if __name__ == '__main__':
    import time
    t1 = time.time()
    font_path = "./Monaco.ttf"
    path = "./test.jpg"
    i = cv.imread(path, 0)
    image = CharPic()
    image.generate_matrix_and_image(i)
    t2 = time.time()
    print(t2 - t1)
    print(image.char_image.shape)
    image.show('')
