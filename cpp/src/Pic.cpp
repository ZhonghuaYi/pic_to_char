#include "Pic.h"
#include "PicProcess.h"
#include <utility>
#include <iostream>

Pic::Pic(Mat img) {
    this->image = std::move(img);
}

Pic::Pic(const string &path) {
    this->image = imread(path);
}

void Pic::show(const string &window_name, int delay) {
    imshow(window_name, this->image);
    waitKey(delay);
}

void Pic::resize(Size size, double fx, double fy) {
    this->image = PicProcess::imageResize(this->image, size, fx, fy);
}

void Pic::saveImage(const string& file_path){
    imwrite(file_path, this->image);
}

Mat Pic::getImage() const {
    return this->image;
}

ColorPic::ColorPic(const Mat &img) {
    if (img.channels() == 1)
        cvtColor(img, this->image, COLOR_GRAY2BGR);
}

ColorPic::ColorPic(Pic const &img) {
    Mat pic_image = img.getImage();
    if (pic_image.channels() == 1)
        cvtColor(pic_image, this->image, COLOR_GRAY2BGR);
}

GrayPic::GrayPic(const Mat &img) {
    this->image = PicProcess::ImageToGray(img);
}

GrayPic::GrayPic(const string &path) {
    this->image = imread(path, 0);
}

GrayPic::GrayPic(const Pic &img) {
    Mat pic_image = img.getImage();
    if (pic_image.channels() == 3)
        cvtColor(pic_image, this->image, COLOR_BGR2GRAY);
}

void BinaryPic::selfThreshold(int method, double thresh) {
    if (method == 0)
        this->th = threshold(this->image, this->image, 0, 255, THRESH_BINARY + THRESH_OTSU);
    else if (method == 1) {
        if (thresh > 0 && thresh < 255)
            this->th = threshold(this->image, this->image, thresh, 255, THRESH_BINARY);
    } else if (method == 2) {
        adaptiveThreshold(this->image, this->image, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 5, 0);
        this->th = -1;
    }
}

BinaryPic::BinaryPic(const Mat &img, int method, double thresh) : GrayPic(img) {
    this->selfThreshold(method, thresh);
}

BinaryPic::BinaryPic(const string &path, int method, double thresh) : GrayPic(path) {
    this->selfThreshold(method, thresh);
}

BinaryPic::BinaryPic(const Pic &img, int method, double thresh) : GrayPic(img) {
    this->selfThreshold(method, thresh);
}

double BinaryPic::getTh() const {
    return this->th;
}

void BinaryPic::resize(Size size, double fx, double fy) {
    Pic::resize(size, fx, fy);
    if (0 < this->th && this->th < 255)
        threshold(this->image, this->image, this->th, 255, THRESH_BINARY);
    else if (this->th == -1)
        adaptiveThreshold(this->image, this->image, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 5, 0);
}

void EdgePic::selfCanny(int th1, int th2) {
    Canny(this->image, this->image, th1, th2);
}

EdgePic::EdgePic(const Mat &img, int th1, int th2) : BinaryPic(img) {
    this->selfCanny(th1, th2);
}

EdgePic::EdgePic(const string &path, int th1, int th2) : BinaryPic(path) {
    this->selfCanny(th1, th2);
}

EdgePic::EdgePic(const Pic &img, int th1, int th2) : BinaryPic(img) {
    this->selfCanny(th1, th2);
}



