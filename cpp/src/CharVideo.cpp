#include "CharVideo.h"


VideoGenerator::VideoGenerator(const string &video_path) {
    this->video = VideoCapture(video_path);
    this->frame_num = this->video.get(CAP_PROP_FRAME_COUNT);
    this->fps = this->video.get(CAP_PROP_FPS);
    Mat f;
    if(this->video.read(f)) {
        this->frame = f;
    }
    else{
        this->flag = 0;
    }
}

Mat VideoGenerator::getFrame() const {
    return this->frame;
}

int VideoGenerator::getFlag() const {
    return this->flag;
}

double VideoGenerator::getFrameNum() const {
    return this->frame_num;
}

double VideoGenerator::getFps() const {
    return this->fps;
}

Mat VideoGenerator::next() {
    Mat f;
    if(this->flag){
        if(this->video.read(f)){
            this->frame = f;
            return f;
        }
        else
            this->flag = 0;
    }
}

Video::Video(const string &path) {
    this->video_path = path;
    this->video_generator = VideoGenerator(path);
    this->frame_num = this->video_generator.getFrameNum();
    this->fps = this->video_generator.getFps();
}

string Video::getVideoPath() {
    return this->video_path;
}

VideoGenerator Video::getVideoGenerator() const {
    return this->video_generator;
}

double Video::getFrameNum() const {
    return this->frame_num;
}

double Video::getFps() const {
    return this->fps;
}

void Video::reload() {
    this->video_generator = VideoGenerator(this->video_path);
}

void Video::play(double speed) {
    int frame_delay = int(1000 / (this->getFps()*speed));
    string window_name = this->video_path;
    while(this->video_generator.getFlag()){
        Mat frame = this->video_generator.getFrame();
        this->video_generator.next();
        imshow(window_name, frame);
        if(char(waitKey(frame_delay)) == 'q')
            break;
    }
}

