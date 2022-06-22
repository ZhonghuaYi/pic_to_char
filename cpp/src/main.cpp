#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <ctime>

#include "Pic.h"
#include "CharPic.h"


int main() {
    using namespace std;
    clock_t start, end;
    start = clock();
    string path = "../test.jpg";
    GrayPic pic(path);
    pic.resize(Size(300, 300));
    Mat gray = pic.getImage();
    CharPic char_pic;
    char_pic.generateCharMatrix(gray, "");
    char_pic.generateCharImage();
    char_pic.resize(Size(200, 100));
    end  = clock();
    cout << float(end-start)/float(CLOCKS_PER_SEC) << "s"<<endl;
    char_pic.show();
    return 0;
}
