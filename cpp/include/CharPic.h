#pragma once

#include "Pic.h"

#include <utility>
#include "PicProcess.h"


class CharPic:public Pic{
protected:
    vector<string> char_matrix;
private:
    int image_flag = 0;
    const string charset= R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";
public:
    CharPic():Pic(){};
    explicit CharPic(Mat img):Pic(std::move(img)){};
    explicit CharPic(const string& path):Pic(path){};
    [[nodiscard]] vector<string> getCharMatrix() const;
    [[nodiscard]] string getCharSet() const;
    [[nodiscard]] int getImageFlag() const;
    void generateCharMatrix(const string& set="");
    void saveCharMatrix(const string& path);
    void loadCharMatrix(const string& path);
    void generateCharImage(const string& font_path="", int font_size=5,
                           const Scalar& background=Scalar(0, 0, 0),
                           const Scalar& color=Scalar(255, 255, 255));
    void generateMatrixAndImage(const string& set="", const string& font_path="", int font_size=5,
                                const Scalar& background=Scalar(0, 0, 0),
                                const Scalar& color=Scalar(255, 255, 255));
};

//const string CharPic::charset = R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";

