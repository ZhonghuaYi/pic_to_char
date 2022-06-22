#include "CharVideo.h"


Video::Video(const string &path) {
    this->video = VideoCapture(path);
    this->frame_num = this->video.get(CAP_PROP_FRAME_COUNT);
    this->fps = this->video.get(CAP_PROP_FPS);
}

string Video::getVideoPath() {
    return this->video_path;
}

VideoCapture Video::getVideo() {
    return this->video;
}

int Video::ChangeVideo(const string& new_path) {
    this->video = VideoCapture(new_path);
    this->video_path = new_path;
    this->frame_num = this->video.get(CAP_PROP_FRAME_COUNT);
    this->fps = this->video.get(CAP_PROP_FPS);
    return 0;
}

long long Video::getFrameNum() {
    return this->frame_num;
}

int Video::getFps() {
    return this->fps;
}
