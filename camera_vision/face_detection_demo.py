"""
Face Detection Demo - Robot detects and looks at faces

This demo uses OpenCV's Haar Cascade classifier to detect faces in the
camera feed and makes the robot turn its head to look at detected faces.

Features:
- Real-time face detection
- Visual feedback (green rectangle around faces)
- Robot head tracking - turns to center largest face
- Face count display
- FPS counter

Usage:
1. Start simulator (reachy-sim)
2. Run this script
3. Show your face to the simulator camera
4. Robot will turn to look at you!
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import cv2
import time
import numpy as np

# ============================================================
# CONSTANTS
# ============================================================

BANNER = """
==================================================
REACHY MINI - FACE DETECTION DEMO
==================================================
"""

# Face detection parameters
SCALE_FACTOR = 1.1  # How much to reduce image size at each scale
MIN_NEIGHBORS = 5   # How many neighbors each candidate rectangle should have
MIN_SIZE = (50, 50)  # Minimum face size

# Robot tracking parameters
TRACKING_THRESHOLD = 30  # Only move head if face is this many pixels from center
TRACKING_SPEED = 0.5     # Duration for head movements (seconds)

# Display parameters
FACE_COLOR = (0, 255, 0)  # Green rectangle for faces
TEXT_COLOR = (0, 255, 0)   # Green text
FONT = cv2.FONT_HERSHEY_SIMPLEX


# ============================================================
# FACE DETECTION
# ============================================================

def init_face_detector():
    """
    Initialize OpenCV face detector using Haar Cascade.

    Returns:
        cv2.CascadeClassifier: Face detector
    """
    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    if face_cascade.empty():
        raise RuntimeError("Failed to load Haar Cascade face detector!")

    return face_cascade


def detect_faces(face_cascade, frame):
    """
    Detect faces in a frame.

    Args:
        face_cascade: OpenCV cascade classifier
        frame: Image frame (BGR)

    Returns:
        list: List of face rectangles [(x, y, w, h), ...]
    """
    # Convert to grayscale (Haar cascades work on grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=MIN_SIZE
    )

    return faces


def draw_face_detection(frame, faces):
    """
    Draw rectangles around detected faces and add labels.

    Args:
        frame: Image frame to draw on
        faces: List of face rectangles

    Returns:
        frame: Frame with face detections drawn
    """
    for i, (x, y, w, h) in enumerate(faces):
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), FACE_COLOR, 2)

        # Add label
        label = f"Face {i + 1}"
        cv2.putText(
            frame,
            label,
            (x, y - 10),
            FONT,
            0.5,
            TEXT_COLOR,
            2
        )

        # Draw center point
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, FACE_COLOR, -1)

    return frame


def get_largest_face(faces):
    """
    Get the largest face (by area) from detected faces.

    Args:
        faces: List of face rectangles

    Returns:
        tuple: (x, y, w, h) of largest face, or None if no faces
    """
    if len(faces) == 0:
        return None

    # Calculate areas and find largest
    areas = [w * h for (x, y, w, h) in faces]
    largest_idx = np.argmax(areas)

    return faces[largest_idx]


# ============================================================
# ROBOT HEAD TRACKING
# ============================================================

def calculate_head_yaw_from_face(face_rect, frame_width):
    """
    Calculate robot head yaw based on face position in frame.

    Args:
        face_rect: (x, y, w, h) of face
        frame_width: Width of camera frame

    Returns:
        float: Yaw angle in degrees (-30 to +30)
    """
    if face_rect is None:
        return 0.0

    x, y, w, h = face_rect

    # Calculate face center
    face_center_x = x + w // 2

    # Calculate offset from frame center (in pixels)
    frame_center_x = frame_width // 2
    offset_x = face_center_x - frame_center_x

    # Convert pixel offset to yaw angle
    # Assume ±320 pixels (half width of 1280x720) maps to ±30 degrees
    max_pixels = frame_width // 2
    max_yaw = 30.0

    yaw = (offset_x / max_pixels) * max_yaw

    # Clamp to safe limits
    yaw = max(-30.0, min(30.0, yaw))

    return yaw


def should_track_face(face_rect, frame_width):
    """
    Determine if robot should move head to track face.

    Only track if face is significantly off-center.

    Args:
        face_rect: (x, y, w, h) of face
        frame_width: Width of camera frame

    Returns:
        bool: True if should track
    """
    if face_rect is None:
        return False

    x, y, w, h = face_rect
    face_center_x = x + w // 2
    frame_center_x = frame_width // 2

    offset = abs(face_center_x - frame_center_x)

    return offset > TRACKING_THRESHOLD


# ============================================================
# MAIN DEMO LOOP
# ============================================================

def run_face_detection(robot):
    """
    Main face detection loop.

    Args:
        robot: Connected ReachyMini instance
    """
    print(BANNER)
    print("🎭 Initializing face detector...")

    # Initialize face detector
    face_cascade = init_face_detector()
    print("✅ Face detector ready!")

    print("\n📷 Starting face detection...")
    print("   Show your face to the camera!")
    print("   Press 'q' to quit\n")

    frame_count = 0
    start_time = time.time()
    current_yaw = 0.0
    last_track_time = 0

    try:
        while True:
            # Get frame from camera
            frame = robot.media.get_frame()

            if frame is None:
                print("⚠️  No frame received")
                time.sleep(0.1)
                continue

            frame_count += 1
            frame_height, frame_width = frame.shape[:2]

            # Detect faces
            faces = detect_faces(face_cascade, frame)

            # Calculate FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            # Draw face detections
            frame = draw_face_detection(frame, faces)

            # Add overlay info
            cv2.putText(
                frame,
                f"Faces Detected: {len(faces)}",
                (10, 30),
                FONT,
                0.7,
                TEXT_COLOR,
                2
            )
            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (10, 60),
                FONT,
                0.6,
                TEXT_COLOR,
                2
            )
            cv2.putText(
                frame,
                f"Head Yaw: {current_yaw:+.1f}°",
                (10, 90),
                FONT,
                0.6,
                TEXT_COLOR,
                2
            )
            cv2.putText(
                frame,
                "Press 'q' to quit",
                (10, frame_height - 20),
                FONT,
                0.6,
                TEXT_COLOR,
                2
            )

            # Track largest face with robot head
            if len(faces) > 0:
                largest_face = get_largest_face(faces)

                # Only track if face is significantly off-center
                # and enough time has passed since last movement
                if should_track_face(largest_face, frame_width):
                    current_time = time.time()
                    if current_time - last_track_time > TRACKING_SPEED:
                        target_yaw = calculate_head_yaw_from_face(
                            largest_face,
                            frame_width
                        )

                        # Move head to look at face
                        head_pose = create_head_pose(
                            roll=0,
                            pitch=0,
                            yaw=target_yaw
                        )

                        robot.goto_target(
                            head=head_pose,
                            duration=TRACKING_SPEED
                        )

                        current_yaw = target_yaw
                        last_track_time = current_time

                        print(f"👁️  Tracking face at yaw: {target_yaw:+.1f}°")

            # Display frame
            cv2.imshow("Reachy Mini - Face Detection", frame)

            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n👋 Quitting...")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")

    finally:
        # Return head to neutral
        print("Returning head to neutral...")
        neutral_head = create_head_pose(0, 0, 0)
        robot.goto_target(head=neutral_head, duration=0.5)
        time.sleep(0.5)

        # Cleanup
        cv2.destroyAllWindows()

        print(f"\n📊 Statistics:")
        print(f"   Total frames: {frame_count}")
        print(f"   Average FPS: {fps:.1f}")
        print(f"   Duration: {elapsed:.1f}s")


# ============================================================
# INITIALIZATION
# ============================================================

def init_robot():
    """
    Initialize robot connection with camera.

    Returns:
        ReachyMini: Connected robot instance
    """
    print(BANNER)
    print("⚠️  Make sure simulator is running in another terminal!")
    print("   (Run: reachy-sim)\n")
    input("Press Enter when simulator is ready...")

    print("\n🔌 Connecting to simulator...")
    robot = ReachyMini(
        localhost_only=True,
        media_backend="default"  # OpenCV camera
    )

    print("✅ Connected to simulator!")

    # Verify camera is available
    if robot.media is None or robot.media.camera is None:
        raise RuntimeError("Camera not available!")

    print("✅ Camera ready!")

    return robot


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Main program."""
    # Initialize robot
    robot = init_robot()

    # Run face detection demo
    run_face_detection(robot)

    print("\nDisconnecting...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
