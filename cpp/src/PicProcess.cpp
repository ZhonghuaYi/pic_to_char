#include "PicProcess.h"

cv::Mat PicProcess::imageResize(cv::Mat image, cv::Size size, double fx, double fy){
    using namespace cv;
    Size new_size = size;
    if (size.width == 0)
        new_size.width = image.cols;
    if (size.height == 0)
        new_size.height = image.rows;
    resize(image, image, new_size);
    if (fx == 1 && fy == 1)
        return image;
    else
        resize(image, image, Size(0, 0), fx, fy);
    return image;
}
