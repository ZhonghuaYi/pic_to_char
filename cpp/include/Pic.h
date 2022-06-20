#pragma once

#include<string>
#include<vector>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

class Pic {
public:
    Pic() : image(Mat()) {};

    explicit Pic(Mat img);

    explicit Pic(const string& path);

    [[nodiscard]] Mat getImage() const;

    void show(const string& window_name = "", int delay = 0);

    virtual void resize(Size size = Size(0, 0), double fx = 1., double fy = 1.);

protected:
    Mat image;
};

class ColorPic : public Pic {
public:
    ColorPic() : Pic() {};

    explicit ColorPic(const Mat& img);

    explicit ColorPic(const string& path) : Pic(path) {};

    explicit ColorPic(const Pic& img);
};

class GrayPic : public Pic {
public:
    GrayPic() : Pic() {};
    explicit GrayPic(const Mat& img);
    explicit GrayPic(const string& path);
    explicit GrayPic(const Pic& img);
};

class BinaryPic : public GrayPic {
protected:
    double th = 0;
    void selfThreshold(int method, double thresh);
public:
    BinaryPic():GrayPic(),th(0){};

    explicit BinaryPic(const Mat& img, int method=0, double thresh=-1);

    explicit BinaryPic(const string& path, int method=0, double thresh=-1);

    explicit BinaryPic(Pic const & img, int method=0, double thresh=-1);

    [[nodiscard]] double getTh() const;

    void resize(Size size, double fx, double fy) override;
};

class EdgePic : public BinaryPic {
protected:
    void selfCanny(int th1, int th2);
public:
    EdgePic() : BinaryPic() {};
    explicit EdgePic(const Mat& img, int th1, int th2);
    explicit EdgePic(const string& path, int th1, int th2);
    explicit EdgePic(const Pic& img, int th1, int th2);
};

class CharPic:public GrayPic{
protected:
    vector<string> char_matrix;
    Mat char_image;
private:
    static const string charset;
public:
    CharPic() : GrayPic() {};
    explicit CharPic(const Mat& img);
    explicit CharPic(const string& path);
    explicit CharPic(const Pic& img);
    [[nodiscard]] vector<string> getCharMatrix() const;
    [[nodiscard]] Mat getCharImage() const;
    [[nodiscard]] static string getCharSet();
    void generateCharMatrix(const string& set="");
    void saveCharMatrix(string path);
};

const string CharPic::charset = R"(.'`^",:Il!i><~+_-?]}1)|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkho*#MW&8%B@$)";
