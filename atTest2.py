"""
Chalmers Phua Jan 2023
"""
from djitellopy import tello
import cv2
from pupil_apriltags import Detector
import tellocontrol as control
import math

airborne = False

control.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

# Create the AprilTag detector for the 36h11 family
at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)

def getUserInputKey():
    left_right, forward_backward, up_down, yaw = 0, 0, 0, 0
    speed = 50  # The drone's movement speed
    if control.getKey("d"): left_right = speed
    if control.getKey("a"): left_right = -speed
    if control.getKey("w"): forward_backward = speed
    if control.getKey("s"): forward_backward = -speed
    if control.getKey("UP"): up_down = speed
    if control.getKey("DOWN"): up_down = -speed
    if control.getKey("RIGHT"): yaw = speed
    if control.getKey("LEFT"): yaw = -speed
    if control.getKey("f"):
        global airborne
        if airborne:
            drone.land()
            airborne = False
        elif not airborne:
            drone.takeoff()
            airborne = True
    return [left_right, forward_backward, up_down, yaw]

def process_image(image, tags, targets):
    for tag in tags:
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        # This part computes the distance between the drone and each targeted tags
        if tag.tag_id in targets:
            W = 0  # The width of the AprilTag(s) to be detected in inches [Replace 0]
            P = math.sqrt((corner_02[0] - corner_01[0]) ** 2 + (corner_02[1] - corner_01[1]) ** 2)
            D_prime = (W * 0) / P  # The calibrated focal length (Can use atTest1.py to calibrate) [Replace 0]
            draw_tag(image, tag, (0, 0, 255), corner_01, corner_02, str(D_prime))
        else:
            draw_tag(image, tag, (0, 255, 0), corner_01, corner_02, "-")
    return image

def draw_tag(image, tag, color, corner_01, corner_02, D_prime):
    center = (int(tag.center[0]), int(tag.center[1]))
    corner_03 = (int(tag.corners[2][0]), int(tag.corners[2][1]))
    corner_04 = (int(tag.corners[3][0]), int(tag.corners[3][1]))
    cv2.circle(image, (center[0], center[1]), 5, color, 5)  # (image, coordinate, radius, color, thickness)
    cv2.line(image, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), color, 2)
    cv2.line(image, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), color, 2)
    cv2.line(image, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), color, 2)
    cv2.line(image, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), color, 2)
    cv2.putText(image, str(tag.tag_id), (center[0] - 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)
    cv2.putText(image, D_prime, (center[0] - 10, center[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)

def target_action(tags, targets):
    for tag in tags:
        if targets.__contains__(tag.tag_id):
            return [0, 0, 0, 0]  # Command the drone's movement here if a targeted tag is detected
    return [0, 0, 0, 0]

while True:
    image = drone.get_frame_read().frame
    debug_image = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(image, estimate_tag_pose=False, camera_params=None, tag_size=None)
    targets = [0, 1, 2]
    debug_image = process_image(debug_image, tags, targets)
    vals = target_action(tags, targets)
    if vals == [0, 0, 0, 0]:
        vals = getUserInputKey()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    cv2.waitKey(1)
    cv2.imshow('Test 2', debug_image)
