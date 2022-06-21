#pragma once

#include "Pic.h"
#include "PicProcess.h"


class CharPic{
protected:
    vector<string> char_matrix;
    Mat char_image;
private:
    static const string charset;
public:
    CharPic(){};
    [[nodiscard]] vector<string> getCharMatrix() const;
    [[nodiscard]] Mat getCharImage() const;
    [[nodiscard]] static string getCharSet();
    void generateCharMatrix(const Mat& gray, const string& set="");
    void saveCharMatrix(const string& path);
};

const string CharPic::charset = R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";

