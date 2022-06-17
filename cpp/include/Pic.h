#pragma once
#include<string>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

class Pic {
public:
	explicit Pic(Mat img);
	explicit Pic(string path);
    Pic(Pic const &img);
    Mat getImage();
	void show(string window_name="", int delay=0);
	void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);

protected:
	Mat image;
};
