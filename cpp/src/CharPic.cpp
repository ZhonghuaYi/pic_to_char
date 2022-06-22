#include "CharPic.h"
#include "PicProcess.h"
#include <fstream>

vector<string> CharPic::getCharMatrix() const {
    return this->char_matrix;
}

Mat CharPic::getCharImage() const {
    return this->char_image;
}

string CharPic::getCharSet() {
    return this->charset;
}

void CharPic::generateCharMatrix(const Mat& gray, const string& set) {
    vector<string> matrix;
    string string_set = set;
    if(set.empty())
        string_set = CharPic::charset;
    int charset_size = int(string_set.size());
    for(int i=0;i<gray.rows;i++){
        string row_char;
        for(int j=0;j<gray.cols;j++){
            int index = int(float(gray.at<uchar>(i, j))/(256 / float(charset_size)));
            row_char.push_back(string_set[index]);
        }
        matrix.push_back(row_char);
    }
    this->char_matrix = matrix;
}

void CharPic::saveCharMatrix(const string& path) {
    ofstream out_file;
    out_file.open(path);
    for(auto& row: char_matrix){
        for(auto& ch: row){
            out_file << ch;
        }
    }
    out_file.close();
}

void CharPic::loadCharMatrix(const string &path) {
    ifstream in_file;
    vector<string> matrix;
    in_file.open(path);
    string s;
    while(getline(in_file, s)){
        matrix.push_back(s);
    }
    this->char_matrix = matrix;
}

void CharPic::generateCharImage(const string &font_path, int font_size, const Scalar& color) {
    int matrix_shape[2] = {int(this->char_matrix.size()), int(this->char_matrix[0].size())};
    Mat canvas;
    if(font_path.empty()){
        Size canvas_size = Size(matrix_shape[0]*7, matrix_shape[0]*7);
        canvas = Mat::zeros(canvas_size, CV_8UC3);
        for(int i=0;i<matrix_shape[0]; ++i){
            for (int j = 0; j < matrix_shape[1]; ++j) {
                string str;
                str.push_back(this->char_matrix[i][j]);
                putText(canvas, str, Point(j*7, i*7), 1, 0.5, color);
            }
        }
    }
    this->char_image = canvas;
}

void CharPic::show(const string &window_name, int delay) {
    imshow(window_name, this->char_image);
    waitKey(delay);
}

void CharPic::resize(Size size, double fx, double fy) {
    this->char_image = PicProcess::imageResize(this->char_image, size, fx, fy);
}

void CharPic::saveImage(const string &file_path) {
    imwrite(file_path, this->char_image);
}

void CharPic::generateMatrixAndImage(const Mat &gray, const string &set, const string &font_path,
                                     int font_size, const Scalar& color) {
    this->generateCharMatrix(gray, set);
    this->generateCharImage(font_path, font_size, color);
}




