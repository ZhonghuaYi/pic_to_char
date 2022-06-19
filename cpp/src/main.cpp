#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

#include "Pic.h"


int main() {
    using namespace std;
    string path = "../test.jpg";
    BinaryPic pic(path);
    Pic* p = &pic;
    p->resize(Size(200, 200));
    p->show();
    return 0;
}
