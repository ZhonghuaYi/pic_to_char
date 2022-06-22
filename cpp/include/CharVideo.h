#pragma once

#include "CharPic.h"

#include <opencv2/videoio.hpp>

using namespace std;

class Video{
protected:
    string video_path;
    VideoCapture video;
    long long frame_num=0;
    int fps = 0;
public:
    explicit Video(const string& path);
    string getVideoPath();
    VideoCapture getVideo();
    int ChangeVideo(const string& new_path);
    long long getFrameNum();
    int getFps();
};
