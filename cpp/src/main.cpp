#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

#include "Pic.h"


int main() {
    using namespace std;
    string path = "../test.jpg";
    EdgePic pic(path, 20, 80);
    pic.show();
    return 0;
}
