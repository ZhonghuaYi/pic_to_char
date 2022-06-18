#include "Pic.h"

Pic::Pic(Mat img)
{
	this->image = img;
}

Pic::Pic(string path)
{
    this->image = imread(path);
}

void Pic::show(string window_name, int delay)
{
    imshow(window_name, this->image);
    waitKey(delay);
}

void Pic::resize(Size size, double fx, double fy)
{
    Size new_size = size;
    if(size.width==0)
        new_size.width = this->image.cols;
    if(size.height==0)
        new_size.height = this->image.rows;
    cv::resize(this->image, this->image, new_size);
    if(fx==1&&fy==1)
        return;
    else
        cv::resize(this->image, this->image, Size(0, 0), fx, fy);
    return;
}

Mat Pic::getImage() const{
    return this->image;
}

ColorPic::ColorPic(Mat img){
    if(img.channels() == 1)
        cvtColor(img, this->image, COLOR_GRAY2BGR);
}

ColorPic::ColorPic(Pic const &img) {
    Mat pic_image = img.getImage();
    if(pic_image.channels() == 1)
        cvtColor(pic_image, this->image, COLOR_GRAY2BGR);
}

GrayPic::GrayPic(Mat img){
    if(img.channels() == 3)
        cvtColor(img, this->image, COLOR_BGR2GRAY);
}

GrayPic::GrayPic(string path){
    this->image = imread(path, 0);
}

GrayPic::GrayPic(const Pic &img){
    Mat pic_image = img.getImage();
    if(pic_image.channels()==3)
        cvtColor(pic_image, this->image, COLOR_BGR2GRAY);
}

BinaryPic::BinaryPic(Mat img) : GrayPic(img) {

}

BinaryPic::BinaryPic(string path) : GrayPic(path) {

}

BinaryPic::BinaryPic(const Pic &img) : GrayPic(img) {

}
