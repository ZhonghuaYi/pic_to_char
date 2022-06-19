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

    virtual void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);

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
    double th = 0;
    void selfThreshold(int method, double thresh);
public:
    BinaryPic():GrayPic(),th(0){};

    explicit BinaryPic(const Mat& img, int method=0, double thresh=-1);

    explicit BinaryPic(const string& path, int method=0, double thresh=-1);

    explicit BinaryPic(Pic const & img, int method=0, double thresh=-1);

    [[nodiscard]] double getTh() const;

    void resize(Size size, double fx, double fy) override;
};

class EdgePic : public BinaryPic {
    protected:
    void selfCanny(int th1, int th2);
public:
    EdgePic() : BinaryPic() {};
    explicit EdgePic(const Mat& img);
};