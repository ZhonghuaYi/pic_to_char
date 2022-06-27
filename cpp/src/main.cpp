#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <ctime>

#include "Pic.h"
#include "CharPic.h"
#include "CharVideo.h"

int main() {
    using namespace std;

    /*
     * char pic test.
     */
//    clock_t start, end;
//    start = clock();
//    string path = "../test.jpg";
//    CharPic char_pic(path);
//    char_pic.resize(Size(200, 200));
//    char_pic.generateMatrixAndImage();
////    char_pic.generateMatrixAndImage("", "", 5, Scalar(255, 0, 0));
//    end  = clock();
//    cout << float(end-start)/float(CLOCKS_PER_SEC) << "s"<<endl;
//    char_pic.show();

    string path = "../test.mp4";
    Video v(path);
    v.play();
    return 0;
}
