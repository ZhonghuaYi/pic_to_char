#pragma once

#include<string>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>
#include <utility>

using namespace std;
using namespace cv;

class Pic {
public:
    Pic() : image(Mat()) {};

    explicit Pic(Mat img);

    explicit Pic(string path);

    Mat getImage() const;

    void show(string window_name = "", int delay = 0);

    void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);

protected:
    Mat image;
};

class ColorPic : public Pic {
public:
    ColorPic() : Pic() {};

    explicit ColorPic(Mat img);

    explicit ColorPic(string path) : Pic(std::move(path)) {};

    explicit ColorPic(Pic const &img);
};

class GrayPic : public Pic {
public:
    GrayPic() : Pic() {};
    explicit GrayPic(Mat img);
    explicit GrayPic(string path);
    explicit GrayPic(Pic const &img);
};

class BinaryPic : public GrayPic {
protected:
    int th;
public:
    BinaryPic():GrayPic(),th(-1){};
    BinaryPic(Mat img);
    BinaryPic(string path);
    BinaryPic(Pic const & img)
};
