#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

#include "Pic.h"


int main() {
    using namespace std;
    string path = "../test.jpg";
    ColorPic image(path);
    GrayPic gray(image);
    cout << gray.getImage().channels() <<endl;
    Mat gray_image = gray.getImage();
    gray.show();
    return 0;
}
