#pragma once

#include "Pic.h"
#include "PicProcess.h"


class CharPic{
protected:
    vector<string> char_matrix;
    Mat char_image;
private:
    const string charset= R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";
public:
    CharPic()= default;
    [[nodiscard]] vector<string> getCharMatrix() const;
    [[nodiscard]] Mat getCharImage() const;
    [[nodiscard]] string getCharSet();
    void generateCharMatrix(const Mat& gray, const string& set="");
    void saveCharMatrix(const string& path);
    void loadCharMatrix(const string& path);
    void generateCharImage(const string& font_path="", int font_size=5, const Scalar& color=Scalar(255, 255, 255));
    void generateMatrixAndImage(const Mat& gray, const string& set="", const string& font_path="",
                                int font_size=5, const Scalar& color=Scalar(255, 255, 255));
    void show(const string& window_name="", int delay=0);
    void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);
    void saveImage(const string& file_path);
};

//const string CharPic::charset = R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";

