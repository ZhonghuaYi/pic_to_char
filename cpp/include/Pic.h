#pragma once

#include<string>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

class Pic {
public:
    Pic() : image(Mat()) {};

    explicit Pic(Mat img);

    explicit Pic(const string& path);

    [[nodiscard]] Mat getImage() const;

    void show(const string& window_name = "", int delay = 0);

    void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);

protected:
    Mat image;
};

class ColorPic : public Pic {
public:
    ColorPic() : Pic() {};

    explicit ColorPic(const Mat& img);

    explicit ColorPic(const string& path) : Pic(path) {};

    explicit ColorPic(const Pic& img);
};

class GrayPic : public Pic {
public:
    GrayPic() : Pic() {};
    explicit GrayPic(const Mat& img);
    explicit GrayPic(const string& path);
    explicit GrayPic(const Pic& img);
};

class BinaryPic : public GrayPic {
protected:
    double th;
public:
    BinaryPic():GrayPic(),th(-1){};

    explicit BinaryPic(const Mat& img, int method=0, double thresh=-1);

    explicit BinaryPic(const string& path, int method=0, double thresh=-1);

    explicit BinaryPic(Pic const & img, int method=0, double thresh=-1);
};
