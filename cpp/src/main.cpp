#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

#include "Pic.h"


int main() {
    using namespace std;
    string path = "../test.jpg";
    Pic image(path);
    image.show();
    return 0;
}
