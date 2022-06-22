#include "PicProcess.h"

cv::Mat PicProcess::ImageToGray(const cv::Mat& image) {
    cv::Mat out;
    if(image.channels()==1){
        out = image;
    }
    else if(image.channels()==3){
        cv::cvtColor(image, out, cv::COLOR_BGR2GRAY);
    }
    return out;
}

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
