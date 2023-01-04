from djitellopy import tello
import cv2
from pupil_apriltags import Detector
import tellocontrol as control

tookoff = False

control.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

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
    speed = 50
    if control.getKey("d"): left_right = speed
    if control.getKey("a"): left_right = -speed
    if control.getKey("w"): forward_backward = speed
    if control.getKey("s"): forward_backward = -speed
    if control.getKey("UP"): up_down = speed
    if control.getKey("DOWN"): up_down = -speed
    if control.getKey("RIGHT"): yaw = speed
    if control.getKey("LEFT"): yaw = -speed
    if control.getKey("f"):
        global tookoff
        if tookoff:
            drone.land()
            tookoff = False
        elif not tookoff:
            drone.takeoff()
            tookoff = True
    if control.getKey("i"): drone.flip_forward()
    if control.getKey("k"): drone.flip_back()
    if control.getKey("j"): drone.flip_left()
    if control.getKey("l"): drone.flip_right()
    return [left_right, forward_backward, up_down, yaw]

while True:
    vals = getUserInputKey()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    image = drone.get_frame_read().frame
    debug_image = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(image, estimate_tag_pose=False, camera_params=None, tag_size=None)
    for tag in tags:
        center = (int(tag.center[0]), int(tag.center[1]))
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        corner_03 = (int(tag.corners[2][0]), int(tag.corners[2][1]))
        corner_04 = (int(tag.corners[3][0]), int(tag.corners[3][1]))
        cv2.circle(debug_image, (center[0], center[1]), 5, (0, 0, 255), 5)
        cv2.line(debug_image, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv2.line(debug_image, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv2.line(debug_image, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv2.line(debug_image, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), (0, 255, 0), 2)
        cv2.putText(debug_image, str(tag.tag_id), (center[0] - 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.waitKey(1)
    cv2.imshow('AprilTag Detection Demo', debug_image)