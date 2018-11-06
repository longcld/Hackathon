#include <iostream>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\core\core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
using namespace std;
using namespace cv;

int main() {
	Mat src = imread("test2.jpg");
	Mat gray;
	cvtColor(src, gray, CV_BGR2GRAY);
	GaussianBlur(gray, gray, Size(9, 9), 2, 2);
	Mat canny;
	Canny(gray, canny, 100, 200, 3, false);
	vector<Vec4i> lines;
	HoughLinesP(canny, lines, 1, CV_PI / 180, 50, 60, 10);
	/*for (int i = 0; i < lines.size(); i++)
	{
		Vec4i l = lines[i];
		line(src, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 2);
	}
	imshow("Anh sau khi tim thay duong thang", src);
	waitKey(0);*/
	//cout << xmin << " " << ymin << " " << xmax << " " << ymax;
	int xmin = 1e9, xmax = 0, ymin = 1e9, ymax = 0;
	for (int i = 0; i < lines.size(); i++) {
		Vec4i l = lines[i];
		xmin = min(xmin, min(l[0], l[2]));
		ymin = min(ymin, min(l[1], l[3]));
		xmax = max(xmax, max(l[0], l[2]));
		ymax = max(ymax, max(l[1], l[3]));
	}
	int width = xmax - xmin;
	Rect r;
	r.x = xmin;
	r.y = ymin;
	r.width = xmax - xmin + 1;
	r.height = ymax - ymin + 1;
	Mat card = Mat(src, r);
	imwrite("idcard.jpg", card);
	/*imshow("The sinh vien", card);
	waitKey(0);*/
	Rect a;
	a.x = 0.2 / 8.5 * r.width;
	a.y = 1.5 / 5.3 * r.height;
	a.width = 1.8 / 8.5 * r.width;
	a.height = 2.5 / 5.3 * r.height;
	Mat subImg = Mat(card, a);
	imshow("The sinh vien", subImg);
	cout << "Kich thuoc cua anh con : " << a.width << " x " << a.height;
	imwrite("Anhcon.jpg", subImg);
	waitKey(0);
	a.x = 0.2 / 8.5 * r.width;
	a.y = 4.2 / 5.3 * r.height;
	a.width = 1.8 / 8.5 * r.width;
	a.height = 0.8 / 5.3 * r.height;
	Mat maSV = Mat(card, a);
	imshow("Ma sinh vien", maSV);
	imwrite("MaSV.jpg", maSV);
	waitKey(0);
	a.x = 2.4 / 8.5 * r.width;
	a.y = 2.3 / 5.3 * r.height;
	a.width = 5.8 / 8.5 * r.width;
	a.height = 2.1 / 5.3 * r.height;
	Mat info = Mat(card, a);
	imshow("Info", info);
	//imwrite("info.jpg", src);
	Mat hsv;
	cvtColor(info, hsv, CV_BGR2HSV);
	Mat mask, element = cv::getStructuringElement(2, cv::Size(3, 3), cv::Point(1, 1));
	inRange(hsv, Scalar(90, 50, 50), Scalar(150, 255, 255), mask);
	imshow("Issnfo", mask);
	imwrite("info.jpg", mask);
	waitKey(0);
	return 0;
}