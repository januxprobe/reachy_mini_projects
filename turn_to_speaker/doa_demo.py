"""
Direction of Arrival (DoA) Demo - Robot Turns Toward Sound

This demo showcases the ReSpeaker microphone array's Direction of Arrival feature.
The robot will:
1. Detect when someone is speaking
2. Determine the direction of the sound (0-360 degrees)
3. Turn its head toward the speaker

⚠️ IMPORTANT DEPLOYMENT NOTE:
This feature requires DIRECT hardware access to the ReSpeaker microphone array.

Mac Development Limitation:
- ❌ Cannot test DoA remotely from Mac (WebRTC/GStreamer issues)
- ✅ Can develop and test the logic/movement code

Production Deployment:
- ✅ Deploy this app to robot via Hugging Face CLI
- ✅ When running ON the robot, DoA works perfectly (direct hardware access)
- ✅ No WebRTC needed when code runs locally on robot

For now, this serves as a reference implementation that will work once deployed to robot.
See README.md for deployment instructions and testing strategy.
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time
import math

# ============================================================
# CONSTANTS
# ============================================================

BANNER = """
==================================================
REACHY MINI - DIRECTION OF ARRIVAL (DoA) DEMO
==================================================
"""

# DoA sampling rate (how often to check for sound direction)
DOA_SAMPLE_INTERVAL = 0.1  # seconds

# Head yaw limits (degrees)
MAX_YAW = 30.0  # Maximum turn left/right
MIN_YAW = -30.0

# Speech detection threshold
SPEECH_CONFIDENCE_THRESHOLD = 0.5  # Adjust if needed


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def angle_to_yaw(doa_angle):
    """
    Convert DoA angle (0-360°, 0=front) to robot head yaw (-30 to +30°).

    DoA Convention:
    - 0° = front (directly in front of robot)
    - 90° = right side
    - 180° = back
    - 270° = left side

    Robot Yaw Convention:
    - 0° = center
    - Positive = turn right
    - Negative = turn left

    Args:
        doa_angle: Direction of Arrival angle (0-360°)

    Returns:
        float: Robot head yaw in degrees, clamped to limits
    """
    # Normalize angle to -180 to +180 range
    if doa_angle > 180:
        normalized = doa_angle - 360
    else:
        normalized = doa_angle

    # Map to robot yaw (with some scaling for natural response)
    # DoA ±90° should map to robot ±30° (full range)
    yaw = normalized / 3.0  # Scale down for smoother response

    # Clamp to robot limits
    yaw = max(MIN_YAW, min(MAX_YAW, yaw))

    return yaw


def display_doa_info(doa_angle, is_speaking, yaw):
    """Display DoA information in a readable format."""
    # Determine direction description
    if 337.5 <= doa_angle or doa_angle < 22.5:
        direction = "FRONT"
    elif 22.5 <= doa_angle < 67.5:
        direction = "FRONT-RIGHT"
    elif 67.5 <= doa_angle < 112.5:
        direction = "RIGHT"
    elif 112.5 <= doa_angle < 157.5:
        direction = "BACK-RIGHT"
    elif 157.5 <= doa_angle < 202.5:
        direction = "BACK"
    elif 202.5 <= doa_angle < 247.5:
        direction = "BACK-LEFT"
    elif 247.5 <= doa_angle < 292.5:
        direction = "LEFT"
    else:
        direction = "FRONT-LEFT"

    # Visual indicator based on direction
    indicators = {
        "FRONT": "    ↑",
        "FRONT-RIGHT": "   ↗",
        "RIGHT": "    →",
        "BACK-RIGHT": "   ↘",
        "BACK": "    ↓",
        "BACK-LEFT": "   ↙",
        "LEFT": "    ←",
        "FRONT-LEFT": "   ↖"
    }

    indicator = indicators.get(direction, "")
    speech_indicator = "🗣️ SPEAKING" if is_speaking else "🔇 Quiet"

    print(f"{speech_indicator} | DoA: {doa_angle:3.0f}° | {direction:12s} {indicator} | Yaw: {yaw:+5.1f}°")


# ============================================================
# MAIN DoA LOOP
# ============================================================

def run_doa_demo(robot):
    """
    Main DoA demonstration loop.

    Continuously monitors the DoA sensor and turns the robot's head
    toward detected speech.

    Args:
        robot: Connected ReachyMini instance
    """
    print("\n🎤 Starting Direction of Arrival Demo")
    print("=" * 70)
    print("Monitoring microphone array for speech...")
    print("Walk around the robot and speak to see it turn toward you!")
    print("\nPress Ctrl+C to stop\n")
    print("=" * 70)
    print()

    try:
        last_yaw = 0.0

        while True:
            # Get DoA data from ReSpeaker array
            doa_data = robot.media.audio.get_DoA()

            # Extract information
            doa_angle = doa_data.get('angle', 0)  # Direction in degrees (0-360)
            is_speaking = doa_data.get('is_speaking', False)  # Speech detected?

            # Convert DoA angle to robot head yaw
            target_yaw = angle_to_yaw(doa_angle)

            # Display current DoA information
            display_doa_info(doa_angle, is_speaking, target_yaw)

            # Only move head if speech is detected and yaw changed significantly
            if is_speaking and abs(target_yaw - last_yaw) > 5.0:
                # Create head pose looking toward sound
                head_pose = create_head_pose(
                    roll=0,
                    pitch=5,  # Slightly up for eye contact
                    yaw=target_yaw
                )

                # Turn head toward speaker
                robot.goto_target(
                    head=head_pose,
                    duration=0.3
                )

                last_yaw = target_yaw
                print(f"   → Turning head to {target_yaw:+5.1f}°")

            # Sample at regular interval
            time.sleep(DOA_SAMPLE_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n👋 Stopping DoA demo...")

        # Return head to neutral position
        print("Returning to neutral position...")
        neutral_head = create_head_pose(0, 0, 0)
        robot.goto_target(head=neutral_head, duration=0.5)
        time.sleep(0.5)


# ============================================================
# INITIALIZATION
# ============================================================

def init_robot():
    """
    Initialize connection to real robot.

    Returns:
        ReachyMini: Connected robot instance
    """
    print(BANNER)
    print("⚠️  IMPORTANT: This demo requires the REAL ROBOT!")
    print("    The simulator doesn't have the ReSpeaker microphone array.\n")

    input("Press Enter to connect to robot...")

    print("\n🤖 Connecting to REAL robot...")
    print("ℹ️  Using default_no_video backend (audio only, no video streaming)")

    # Connect to real robot
    # Use default_no_video to get audio/DoA access without video streaming issues
    robot = ReachyMini(localhost_only=False, media_backend="default_no_video")

    print("✅ Connected to real robot!")

    # Verify audio interface is available
    if robot.media is None or robot.media.audio is None:
        print("\n❌ ERROR: Audio interface not available!")
        print("   The media backend did not initialize properly.")
        print("\n   Possible solutions:")
        print("   1. Check if robot's audio hardware is functioning")
        print("   2. Try restarting the robot")
        print("   3. Check robot dashboard: http://reachy-mini.local:8000/")
        raise RuntimeError("Audio interface not available - cannot access DoA")

    print("✅ Audio interface ready!")
    print("✅ Ready to detect sound direction!\n")

    return robot


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Main program - initializes robot and runs DoA demo."""
    # Initialize robot
    robot = init_robot()

    # Run DoA demonstration
    run_doa_demo(robot)

    print("Disconnecting robot...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
