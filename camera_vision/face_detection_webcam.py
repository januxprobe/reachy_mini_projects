"""
Face Detection Demo - Using Mac Webcam + Simulator Robot

This version uses your Mac's webcam for face detection while controlling
the robot in the simulator. Perfect for development!

Setup:
- Robot runs in simulator (movements)
- Webcam detects your face
- Robot turns head as if it's looking at you

This lets you test face detection without needing objects in the simulator!
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
REACHY MINI - FACE DETECTION (WEBCAM VERSION)
==================================================
"""

# Face detection parameters
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_SIZE = (50, 50)

# Robot tracking parameters
TRACKING_THRESHOLD = 5  # Lowered from 30 to 5 - more sensitive!
TRACKING_SPEED = 0.5

# Display parameters
FACE_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 255, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX


# ============================================================
# FACE DETECTION (Same as before)
# ============================================================

def init_face_detector():
    """Initialize OpenCV face detector using Haar Cascade."""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    if face_cascade.empty():
        raise RuntimeError("Failed to load Haar Cascade face detector!")
    return face_cascade


def detect_faces(face_cascade, frame):
    """Detect faces in a frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=MIN_SIZE
    )
    return faces


def draw_face_detection(frame, faces):
    """Draw rectangles around detected faces."""
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x + w, y + h), FACE_COLOR, 2)
        label = f"Face {i + 1}"
        cv2.putText(frame, label, (x, y - 10), FONT, 0.5, TEXT_COLOR, 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, FACE_COLOR, -1)
    return frame


def get_largest_face(faces):
    """Get the largest face by area."""
    if len(faces) == 0:
        return None
    areas = [w * h for (x, y, w, h) in faces]
    largest_idx = np.argmax(areas)
    return faces[largest_idx]


def calculate_head_yaw_from_face(face_rect, frame_width):
    """Calculate robot head yaw based on face position."""
    if face_rect is None:
        return 0.0

    x, y, w, h = face_rect
    face_center_x = x + w // 2
    frame_center_x = frame_width // 2
    offset_x = face_center_x - frame_center_x

    max_pixels = frame_width // 2
    max_yaw = 30.0
    yaw = (offset_x / max_pixels) * max_yaw
    yaw = max(-30.0, min(30.0, yaw))

    return yaw


def should_track_face(face_rect, frame_width):
    """Determine if robot should move head to track face."""
    if face_rect is None:
        return False

    x, y, w, h = face_rect
    face_center_x = x + w // 2
    frame_center_x = frame_width // 2
    offset = abs(face_center_x - frame_center_x)

    return offset > TRACKING_THRESHOLD


# ============================================================
# WEBCAM CAPTURE
# ============================================================

def init_webcam():
    """
    Initialize Mac webcam using OpenCV.

    Returns:
        cv2.VideoCapture: Webcam capture object
    """
    print("📷 Opening Mac webcam...")

    # Try to open default webcam (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Failed to open webcam! Make sure it's not in use by another app.")

    # Set resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Get actual resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"✅ Webcam opened: {width}x{height}")

    return cap


# ============================================================
# MAIN DEMO LOOP
# ============================================================

def run_face_detection(robot, webcam):
    """
    Main face detection loop using webcam.

    Args:
        robot: Connected ReachyMini instance
        webcam: OpenCV VideoCapture for webcam
    """
    print("\n🎭 Initializing face detector...")
    face_cascade = init_face_detector()
    print("✅ Face detector ready!")

    print("\n📷 Starting face detection...")
    print("   Look at your webcam!")
    print("   Press 'q' to quit\n")

    frame_count = 0
    start_time = time.time()
    current_yaw = 0.0
    last_track_time = 0

    try:
        while True:
            # Get frame from WEBCAM (not robot camera!)
            ret, frame = webcam.read()

            if not ret:
                print("⚠️  Failed to read from webcam")
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
            cv2.putText(frame, f"Faces Detected: {len(faces)}", (10, 30), FONT, 0.7, TEXT_COLOR, 2)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), FONT, 0.6, TEXT_COLOR, 2)
            cv2.putText(frame, f"Robot Yaw: {current_yaw:+.1f}°", (10, 90), FONT, 0.6, TEXT_COLOR, 2)
            cv2.putText(frame, "Webcam Feed (not robot camera)", (10, 120), FONT, 0.5, (255, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, frame_height - 20), FONT, 0.6, TEXT_COLOR, 2)

            # Track largest face with robot head (in simulator)
            if len(faces) > 0:
                largest_face = get_largest_face(faces)

                # Calculate target yaw for display (even if not moving)
                target_yaw = calculate_head_yaw_from_face(largest_face, frame_width)

                if should_track_face(largest_face, frame_width):
                    current_time = time.time()
                    if current_time - last_track_time > TRACKING_SPEED:
                        # Move robot head in simulator
                        head_pose = create_head_pose(roll=0, pitch=0, yaw=target_yaw)
                        robot.goto_target(head=head_pose, duration=TRACKING_SPEED)

                        current_yaw = target_yaw
                        last_track_time = current_time
                        print(f"👁️  Tracking face at yaw: {target_yaw:+.1f}°")
                else:
                    # Face is centered - update display but don't move
                    current_yaw = target_yaw

            # Display webcam feed
            cv2.imshow("Face Detection - Webcam Feed", frame)

            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n👋 Quitting...")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")

    finally:
        # Return robot head to neutral
        print("Returning robot head to neutral...")
        neutral_head = create_head_pose(0, 0, 0)
        robot.goto_target(head=neutral_head, duration=0.5)
        time.sleep(0.5)

        # Cleanup
        webcam.release()
        cv2.destroyAllWindows()

        print(f"\n📊 Statistics:")
        print(f"   Total frames: {frame_count}")
        print(f"   Average FPS: {fps:.1f}")
        print(f"   Duration: {elapsed:.1f}s")


# ============================================================
# INITIALIZATION
# ============================================================

def init_robot():
    """Initialize robot connection to simulator."""
    print(BANNER)
    print("⚠️  Make sure simulator is running in another terminal!")
    print("   (Run: reachy-sim)\n")
    input("Press Enter when simulator is ready...")

    print("\n🔌 Connecting to simulator...")
    robot = ReachyMini(
        localhost_only=True,
        media_backend="no_media"  # We don't need robot camera!
    )

    print("✅ Connected to simulator!")
    return robot


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Main program."""
    # Initialize robot (for movement control)
    robot = init_robot()

    # Initialize webcam (for face detection)
    webcam = init_webcam()

    # Run face detection demo
    run_face_detection(robot, webcam)

    print("\nDisconnecting...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
