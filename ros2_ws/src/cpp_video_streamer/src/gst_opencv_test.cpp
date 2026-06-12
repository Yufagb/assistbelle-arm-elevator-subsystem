#include <opencv2/opencv.hpp>
#include <gst/gst.h>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    // === GStreamer pipeline (YUYV 640x480 30fps) ===
    std::string pipeline =
        "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! appsink";

    cv::VideoCapture cap(pipeline, cv::CAP_GSTREAMER);

    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open camera pipeline.\n";
        return -1;
    }
    std::cout << "Camera opened successfully.\n";

    cv::Mat frame, hsv, mask, result;
    int frame_count = 0;

    // Adjusted yellow range
    cv::Scalar lower_yellow(15, 100, 100);  // H lower, S lower, V lower
    cv::Scalar upper_yellow(35, 255, 255);  // H upper, S upper, V upper

    while (true) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Warning: Empty frame captured.\n";
            continue;
        }

        // Convert to HSV
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        // Threshold yellow
        cv::inRange(hsv, lower_yellow, upper_yellow, mask);

        // Clean mask
        cv::erode(mask, mask, cv::Mat(), cv::Point(-1,-1), 1);
        cv::dilate(mask, mask, cv::Mat(), cv::Point(-1,-1), 1);

        // Bitwise AND to see filtered colors
        cv::bitwise_and(frame, frame, result, mask);

        // Find contours
        std::vector<std::vector<cv::Point>> contours;
        cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        for (const auto &contour : contours) {
            // Ignore small contours
            if (cv::contourArea(contour) < 500)
                continue;

            // Get bounding box
            cv::Rect bbox = cv::boundingRect(contour);

            // Draw bounding box on original frame
            cv::rectangle(frame, bbox, cv::Scalar(0, 0, 255), 2); // red box, thickness 2

            // Print a few points inside the contour
            for (size_t i = 0; i < contour.size(); i += std::max<size_t>(1, contour.size()/5)) {
                std::cout << "Pixel: (" << contour[i].x << "," << contour[i].y << ")\n";
            }
        }

        // Show images
        cv::imshow("Original", frame);
        cv::imshow("Mask", mask);
        //cv::imshow("Filtered", result);

        if (cv::waitKey(1) == 27) break;  // ESC to quit

        frame_count++;
    }

    cap.release();
    return 0;
}
