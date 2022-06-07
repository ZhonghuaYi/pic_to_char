#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>



char grayscaleToChar(const std::string& map, int grayscale, int gray_level){
    int step = int(round(gray_level / map.length()));
    int index = grayscale / step;
    return map[index];
}


cv::Mat imageToChar(const std::string& map, const cv::Mat& img, int gray_level){
    cv::Mat index = img.clone();

}



int main() {
    const static std::string map = "@B%8WM#*oahkbdpwmZO0QLCJUYXzcunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. ";
    std::cout << "@B%8WM#*oahkbdpwmZO0QLCJUYXzcunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. " << std::endl;
    return 0;
}
