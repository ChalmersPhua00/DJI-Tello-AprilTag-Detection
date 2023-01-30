"""
Chalmers Phua Dec 2022
"""
import math
import cv2
from pupil_apriltags import Detector

def main():
    # Doc: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a57c0e81e83e60f36c83027dc2a188e80
    cap = cv2.VideoCapture(0)

    # Src: https://pypi.org/project/pupil-apriltags/
    at_detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0
    )

    # Src: https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample/blob/main/sample.py
    while True:
        ret, image = cap.read()
        if not ret:
            break
        debug_image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(image, estimate_tag_pose=False, camera_params=None, tag_size=None)
        debug_image = process_image(debug_image, tags, [0, 1, 2])
        cv2.waitKey(1)
        cv2.imshow('Test 1', debug_image)

def process_image(image, tags, targets):
    for tag in tags:
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        if tag.tag_id in targets:
            draw_tag(image, tag, (0, 0, 255), corner_01, corner_02)
            # Src: https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
            W = 0   # The width of the AprilTag(s) to be detected in inches [Replace 0]
            D = 0  # The distance between the drone and the AprilTag for calibration only [Replace 0]
            P = math.sqrt((corner_02[0] - corner_01[0]) ** 2 + (corner_02[1] - corner_01[1]) ** 2)
            #F = (P * D) / W = 955  # Uncomment for calibration by computing the focal length F
            D_prime = (W * 0) / P  # The calibrated focal length [Replace 0]
        else:
            draw_tag(image, tag, (0, 255, 0), corner_01, corner_02)
    return image

def draw_tag(image, tag, color, corner_01, corner_02):
    center = (int(tag.center[0]), int(tag.center[1]))
    corner_03 = (int(tag.corners[2][0]), int(tag.corners[2][1]))
    corner_04 = (int(tag.corners[3][0]), int(tag.corners[3][1]))
    # Doc: https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html
    cv2.circle(image, (center[0], center[1]), 5, color, 5)  # (image, coordinate, radius, color, thickness)
    cv2.line(image, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), color, 2)
    cv2.line(image, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), color, 2)
    cv2.line(image, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), color, 2)
    cv2.line(image, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), color, 2)
    cv2.putText(image, str(tag.tag_id), (center[0] - 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)

if __name__ == "__main__":
    main()