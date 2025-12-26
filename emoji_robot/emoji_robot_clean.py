"""
Emoji Robot - Express Emotions with Reachy Mini

A clean, well-structured program that lets you control your robot's emotions.
Press keys to trigger different emotional expressions!
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time
import os


# ============================================================
# CONSTANTS
# ============================================================

BANNER = """
==================================================
REACHY MINI - EMOJI ROBOT
==================================================
"""

EMOTION_MENU = """
Press a key to show emotion:
  h - Happy
  s - Sad
  e - Excited
  c - Curious
  q - Quit
"""


# ============================================================
# EMOTION FUNCTIONS
# ============================================================

def show_happy(robot):
    """Express happiness - looking up with antennas raised."""
    print("😊 Showing HAPPY emotion!")

    head_pose = create_head_pose(roll=0, pitch=15, yaw=0)
    robot.goto_target(
        head=head_pose,
        antennas=[0.8, 0.8],
        duration=0.5
    )
    time.sleep(0.5)
    print("   Done!")


def show_sad(robot):
    """Express sadness - looking down with droopy antennas."""
    print("😢 Showing SAD emotion...")

    head_pose = create_head_pose(roll=0, pitch=-20, yaw=0)
    robot.goto_target(
        head=head_pose,
        antennas=[-0.8, -0.8],
        duration=0.8
    )
    time.sleep(0.8)
    print("   Done!")


def show_excited(robot):
    """Express excitement - fast nodding with wiggling antennas."""
    print("🤩 Showing EXCITED emotion!")

    for _ in range(3):
        # Nod up
        head_up = create_head_pose(roll=0, pitch=10, yaw=0)
        robot.goto_target(head=head_up, antennas=[1.0, -1.0], duration=0.2)
        time.sleep(0.2)

        # Nod down
        head_down = create_head_pose(roll=0, pitch=-10, yaw=0)
        robot.goto_target(head=head_down, antennas=[-1.0, 1.0], duration=0.2)
        time.sleep(0.2)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.3)
    time.sleep(0.3)
    print("   Done!")


def show_curious(robot):
    """Express curiosity - tilting head side to side."""
    print("🤔 Showing CURIOUS emotion!")

    # Define head poses
    head_right = create_head_pose(roll=20, pitch=5, yaw=0)
    head_left = create_head_pose(roll=-20, pitch=5, yaw=0)

    # Tilt right
    robot.goto_target(head=head_right, antennas=[0.6, -0.3], duration=0.6)
    time.sleep(0.6)

    # Tilt left
    robot.goto_target(head=head_left, antennas=[-0.3, 0.6], duration=0.6)
    time.sleep(0.6)

    # Tilt right again
    robot.goto_target(head=head_right, antennas=[0.6, -0.3], duration=0.6)
    time.sleep(0.6)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    robot.goto_target(head=neutral_head, antennas=[0, 0], duration=0.5)
    time.sleep(0.5)
    print("   Done!")


# ============================================================
# INITIALIZATION
# ============================================================

def init_robot():
    """
    Initialize robot connection.

    Returns:
        ReachyMini: Connected robot instance
    """
    print(BANNER)
    print("Choose mode:")
    print("  1 - Real Robot (wireless)")
    print("  2 - Simulation (no robot needed)")
    print()

    while True:
        mode = input("Enter 1 or 2: ").strip()

        if mode == "1":
            print("\n🤖 Connecting to REAL robot...")
            robot = ReachyMini(localhost_only=False, media_backend="no_media")
            print("✅ Connected to real robot!")
            return robot

        elif mode == "2":
            print("\n🎮 Starting SIMULATION...")
            print("(Make sure simulator daemon is running!)")
            input("Press Enter when ready...")
            robot = ReachyMini(localhost_only=True, media_backend="no_media")
            print("✅ Connected to simulator!")
            return robot

        else:
            print("❌ Invalid choice! Enter 1 or 2")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Main program loop - handles user input and emotion selection."""
    # Initialize robot
    robot = init_robot()

    # Display menu
    print("\n🤖 Robot is ready to show emotions!")
    print(EMOTION_MENU)

    # Emotion mapping
    emotions = {
        'h': show_happy,
        's': show_sad,
        'e': show_excited,
        'c': show_curious
    }

    # Main interaction loop
    try:
        while True:
            user_input = input("Choose emotion (h/s/e/c/q): ").lower().strip()

            if user_input == 'q':
                print("\n👋 Goodbye!")
                print("Disconnecting robot...")
                os._exit(0)

            elif user_input in emotions:
                emotions[user_input](robot)
                print()  # Empty line for readability

            else:
                print("❌ Invalid choice! Try h, s, e, c, or q")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        print("Disconnecting robot...")
        os._exit(0)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
