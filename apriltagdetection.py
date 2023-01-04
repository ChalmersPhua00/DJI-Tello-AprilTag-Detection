"""
Chalmers Phua Dec 2022
Basic AprilTag detection program using computer's webcam
"""
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
        debug_image = draw_tags(debug_image, tags)
        cv2.waitKey(1)
        cv2.imshow('AprilTag Detection Demo', debug_image)

def draw_tags(image, tags):
    for tag in tags:
        center = (int(tag.center[0]), int(tag.center[1]))
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        corner_03 = (int(tag.corners[2][0]), int(tag.corners[2][1]))
        corner_04 = (int(tag.corners[3][0]), int(tag.corners[3][1]))
        # Doc: https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html
        cv2.circle(image, (center[0], center[1]), 5, (0, 0, 255), 5) # (image, coordinate, radius, color, thickness)
        cv2.line(image, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv2.line(image, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv2.line(image, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv2.line(image, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), (0, 255, 0), 2)
        cv2.putText(image, str(tag.tag_id), (center[0] - 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    return image

if __name__ == "__main__":
    main()