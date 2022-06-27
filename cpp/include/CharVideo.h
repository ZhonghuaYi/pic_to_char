#pragma once

#include "CharPic.h"

#include <opencv2/videoio.hpp>

using namespace std;
using namespace cv;


class VideoGenerator{
private:
    VideoCapture video;
    Mat frame;
    double frame_num=0;
    double fps = 0;
    int flag = 1;
public:
    VideoGenerator()= default;
    explicit VideoGenerator(const string& video_path);
    [[nodiscard]] Mat getFrame() const;
    [[nodiscard]] int getFlag() const;
    [[nodiscard]] double getFrameNum() const;
    [[nodiscard]] double getFps() const;
    Mat next();
};

class Video{
protected:
    string video_path;
    VideoGenerator video_generator;
    double frame_num=0;
    double fps = 0;
public:
    explicit Video(const string& path);
    string getVideoPath();
    [[nodiscard]] VideoGenerator getVideoGenerator() const;
    [[nodiscard]] double getFrameNum() const;
    [[nodiscard]] double getFps() const;
    void reload();
    void play(double speed=1);
};

class CharVideo:public Video{
protected:
    Mat
};
