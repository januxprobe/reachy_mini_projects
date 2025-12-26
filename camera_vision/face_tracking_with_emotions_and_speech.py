"""
Face Tracking with Emotions AND Speech - Interactive Robot Behavior

This demo combines face detection with emoji robot emotions AND speech,
creating a fully interactive and expressive robot that responds to people.

Behaviors:
- Shows CURIOUS emotion + says "Hello! Who are you?" when first detecting face
- Shows HAPPY emotion + says "I'm so happy to see you!" when person stays
- Shows SAD emotion + says "Goodbye! Come back soon!" when person leaves
- Tracks face with head movements continuously

Perfect for: Interactive demonstrations, testing emotion + speech integration
"""

import sys
import os
import subprocess
from pathlib import Path

# Add emoji_robot to path so we can import emotion functions
emoji_robot_path = os.path.join(os.path.dirname(__file__), '..', 'emoji_robot')
sys.path.insert(0, emoji_robot_path)

from emoji_robot_clean import show_happy, show_sad, show_curious

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
REACHY MINI - FACE TRACKING WITH EMOTIONS & SPEECH
==================================================
"""

# Speech phrases for face tracking interactions
SPEECH_PHRASES = {
    'curious': "Hello! Who are you?",
    'happy': "I'm so happy to see you!",
    'sad': "Goodbye! Come back soon!"
}

# Temporary directory for generated speech files
TEMP_SPEECH_DIR = Path(__file__).parent / "temp_speech"

# Face detection parameters
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_SIZE = (50, 50)

# Robot tracking parameters
TRACKING_THRESHOLD = 5
TRACKING_SPEED = 0.5

# Emotion behavior parameters
EMOTION_COOLDOWN = 5.0      # Seconds between emotions
HAPPY_TRIGGER_TIME = 3.0    # Show happy after this many seconds
GOODBYE_DELAY = 2.0          # Wait before showing sad when face disappears

# Display parameters
FACE_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 255, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX


# ============================================================
# FACE DETECTION (Same as before)
# ============================================================

def init_face_detector():
    """Initialize OpenCV face detector."""
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


def draw_face_detection(frame, faces, emotion_state):
    """Draw rectangles around detected faces and show emotion state."""
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x + w, y + h), FACE_COLOR, 2)
        label = f"Face {i + 1}"
        cv2.putText(frame, label, (x, y - 10), FONT, 0.5, TEXT_COLOR, 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, FACE_COLOR, -1)

    # Show current emotion state
    emotion_text = f"Emotion: {emotion_state}"
    cv2.putText(frame, emotion_text, (10, 150), FONT, 0.6, (255, 255, 0), 2)

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
    """Initialize Mac webcam."""
    print("📷 Opening Mac webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Failed to open webcam!")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"✅ Webcam opened: {width}x{height}")

    return cap


# ============================================================
# SPEECH GENERATION
# ============================================================

def setup_speech_directory():
    """Create temporary directory for speech files if it doesn't exist."""
    TEMP_SPEECH_DIR.mkdir(parents=True, exist_ok=True)


def generate_speech(text, emotion_name):
    """
    Generate speech using macOS 'say' command and convert to WAV.

    Args:
        text: The text to convert to speech
        emotion_name: Name of the emotion (for filename)

    Returns:
        Path: Path to the generated WAV file
    """
    aiff_file = TEMP_SPEECH_DIR / f"{emotion_name}_greeting.aiff"
    wav_file = TEMP_SPEECH_DIR / f"{emotion_name}_greeting.wav"

    try:
        # Generate speech using macOS 'say' command (outputs AIFF)
        subprocess.run(
            ['say', '-o', str(aiff_file), text],
            check=True,
            capture_output=True
        )

        # Convert AIFF to WAV using ffmpeg (robot expects WAV)
        subprocess.run(
            ['ffmpeg', '-i', str(aiff_file), '-y', str(wav_file)],
            check=True,
            capture_output=True
        )

        return wav_file
    except Exception as e:
        print(f"⚠️  Speech generation error: {e}")
        return None


def play_speech_for_emotion(robot, emotion_name):
    """
    Generate and play speech for a given emotion.

    Args:
        robot: ReachyMini robot instance
        emotion_name: Name of the emotion (key in SPEECH_PHRASES)
    """
    try:
        # Get the phrase for this emotion
        phrase = SPEECH_PHRASES[emotion_name]

        # Generate speech file
        speech_file = generate_speech(phrase, emotion_name)

        if speech_file and speech_file.exists():
            # Play through robot.media.play_sound() (consistent with emoji_robot)
            robot.media.play_sound(str(speech_file))
            print(f"   🔊 \"{phrase}\"")
        else:
            print(f"   ⚠️ Could not generate speech for {emotion_name}")

    except Exception as e:
        print(f"   ⚠️ Speech playback error: {e}")


# ============================================================
# EMOTION STATE MACHINE
# ============================================================

class EmotionStateMachine:
    """Manages robot emotion states based on face detection."""

    def __init__(self, robot):
        self.robot = robot
        self.state = "NEUTRAL"  # NEUTRAL, CURIOUS, HAPPY, SAD
        self.face_detected = False
        self.was_face_detected = False
        self.face_first_seen_time = None
        self.face_last_seen_time = None
        self.last_emotion_time = 0
        self.emotion_in_progress = False

    def update(self, faces_detected):
        """
        Update emotion state based on face detection.

        Args:
            faces_detected: Boolean, True if faces are detected

        Returns:
            str: Current emotion state
        """
        current_time = time.time()
        self.was_face_detected = self.face_detected
        self.face_detected = faces_detected

        # Don't trigger emotions if one is in progress or too soon
        if self.emotion_in_progress:
            return self.state

        if current_time - self.last_emotion_time < EMOTION_COOLDOWN:
            return self.state

        # Face just appeared (CURIOUS)
        if self.face_detected and not self.was_face_detected:
            self.face_first_seen_time = current_time
            self.face_last_seen_time = current_time
            self._trigger_emotion("CURIOUS")
            print("👀 New face detected! Showing CURIOUS emotion...")
            return self.state

        # Face still present - update timer
        if self.face_detected:
            self.face_last_seen_time = current_time

            # Face been there a while (HAPPY)
            time_since_first_seen = current_time - self.face_first_seen_time
            if (time_since_first_seen >= HAPPY_TRIGGER_TIME and
                self.state != "HAPPY"):
                self._trigger_emotion("HAPPY")
                print("😊 Person staying! Showing HAPPY emotion...")
                return self.state

        # Face just disappeared (SAD)
        if not self.face_detected and self.was_face_detected:
            if self.face_last_seen_time:
                time_since_last_seen = current_time - self.face_last_seen_time
                if time_since_last_seen >= GOODBYE_DELAY:
                    self._trigger_emotion("SAD")
                    print("👋 Person left! Showing SAD emotion...")
                    self.face_first_seen_time = None
                    return self.state

        return self.state

    def _trigger_emotion(self, emotion):
        """Trigger an emotion (will be executed in main loop)."""
        self.state = emotion
        self.last_emotion_time = time.time()

    def execute_emotion(self):
        """Execute the current emotion with speech if needed."""
        if self.state == "NEUTRAL" or self.emotion_in_progress:
            return

        self.emotion_in_progress = True

        try:
            # Play speech first (non-blocking), then show emotion
            if self.state == "CURIOUS":
                play_speech_for_emotion(self.robot, 'curious')
                show_curious(self.robot)
            elif self.state == "HAPPY":
                play_speech_for_emotion(self.robot, 'happy')
                show_happy(self.robot)
            elif self.state == "SAD":
                play_speech_for_emotion(self.robot, 'sad')
                show_sad(self.robot)

            # Return to neutral state after emotion
            self.state = "NEUTRAL"

        finally:
            self.emotion_in_progress = False


# ============================================================
# MAIN DEMO LOOP
# ============================================================

def run_face_tracking_with_emotions(robot, webcam):
    """Main demo loop with emotions."""
    print("\n🎭 Initializing face detector...")
    face_cascade = init_face_detector()
    print("✅ Face detector ready!")

    print("\n📷 Starting face tracking with emotions...")
    print("   Look at your webcam and watch robot respond!")
    print("   Press 'q' to quit\n")

    # Initialize emotion state machine
    emotion_machine = EmotionStateMachine(robot)

    frame_count = 0
    start_time = time.time()
    current_yaw = 0.0
    last_track_time = 0

    try:
        while True:
            # Get frame from webcam
            ret, frame = webcam.read()

            if not ret:
                print("⚠️  Failed to read from webcam")
                time.sleep(0.1)
                continue

            frame_count += 1
            frame_height, frame_width = frame.shape[:2]

            # Detect faces
            faces = detect_faces(face_cascade, frame)
            faces_detected = len(faces) > 0

            # Update emotion state
            emotion_state = emotion_machine.update(faces_detected)

            # Execute emotion if triggered (non-blocking check)
            if not emotion_machine.emotion_in_progress:
                emotion_machine.execute_emotion()

            # Calculate FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            # Draw face detections
            frame = draw_face_detection(frame, faces, emotion_state)

            # Add overlay info
            cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), FONT, 0.7, TEXT_COLOR, 2)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), FONT, 0.6, TEXT_COLOR, 2)
            cv2.putText(frame, f"Robot Yaw: {current_yaw:+.1f}°", (10, 90), FONT, 0.6, TEXT_COLOR, 2)
            cv2.putText(frame, "State: " + emotion_state, (10, 120), FONT, 0.6, (255, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, frame_height - 20), FONT, 0.6, TEXT_COLOR, 2)

            # Track largest face (only when not showing emotion)
            if faces_detected and not emotion_machine.emotion_in_progress:
                largest_face = get_largest_face(faces)
                target_yaw = calculate_head_yaw_from_face(largest_face, frame_width)

                if should_track_face(largest_face, frame_width):
                    current_time = time.time()
                    if current_time - last_track_time > TRACKING_SPEED:
                        head_pose = create_head_pose(roll=0, pitch=0, yaw=target_yaw)
                        robot.goto_target(head=head_pose, duration=TRACKING_SPEED)
                        current_yaw = target_yaw
                        last_track_time = current_time
                else:
                    current_yaw = target_yaw

            # Display webcam feed
            cv2.imshow("Face Tracking with Emotions", frame)

            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n👋 Quitting...")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")

    finally:
        # Return robot to neutral
        print("Returning to neutral...")
        neutral_head = create_head_pose(0, 0, 0)
        robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
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
    """Initialize robot connection and speech system."""
    print(BANNER)

    # Setup speech directory
    print("🔊 Setting up speech system...")
    setup_speech_directory()
    print("✅ Speech system ready!")

    print("\n⚠️  Make sure simulator is running!")
    print("   (Run: reachy-sim)\n")
    input("Press Enter when simulator is ready...")

    print("\n🔌 Connecting to simulator...")
    robot = ReachyMini(
        localhost_only=True,
        media_backend="default_no_video"  # Audio support for speech playback
    )

    print("✅ Connected to simulator!")
    print("✅ Audio system ready!")
    return robot


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Main program."""
    robot = init_robot()
    webcam = init_webcam()
    run_face_tracking_with_emotions(robot, webcam)
    print("\nDisconnecting...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
