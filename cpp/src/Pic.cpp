#include "Pic.h"

Pic::Pic(Mat img)
{
	this->image = img;
}

Pic::Pic(string path)
{
    this->image = imread(path);
}

Pic::Pic(const Pic &img) {
    this->image = img.image;
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

Mat Pic::getImage() {
    return this->image;
}


