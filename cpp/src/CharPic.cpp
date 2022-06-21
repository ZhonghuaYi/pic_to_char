#include "CharPic.h"
#include <fstream>

vector<string> CharPic::getCharMatrix() const {
    return this->char_matrix;
}

Mat CharPic::getCharImage() const {
    return this->char_image;
}

string CharPic::getCharSet() {
    return CharPic::charset;
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
            int index = int(gray.at<uchar>(i, j)/(256 / charset_size));
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
