#pragma once

#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>

namespace PicProcess{
    cv::Mat ImageToGray(const cv::Mat& image);
    cv::Mat imageResize(cv::Mat image, cv::Size size = cv::Size(0, 0), double fx = 1., double fy = 1.);
};
