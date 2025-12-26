"""
Emoji Robot - Express Emotions with Reachy Mini

This program lets you control your robot's emotions using keyboard keys:
- h: Happy
- s: Sad
- e: Excited
- c: Curious
- q: Quit
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time
import os

# Choose between simulation or real robot
print("=" * 50)
print("REACHY MINI - EMOJI ROBOT")
print("=" * 50)
print()
print("Choose mode:")
print("  1 - Real Robot (wireless)")
print("  2 - Simulation (no robot needed)")
print()

while True:
    mode = input("Enter 1 or 2: ").strip()
    if mode == "1":
        print("\n🤖 Connecting to REAL robot...")
        mini = ReachyMini(localhost_only=False, media_backend="no_media")
        print("✅ Connected to real robot!")
        break
    elif mode == "2":
        print("\n🎮 Starting SIMULATION...")
        print("(Make sure to run: uv run reachy-mini-daemon --sim)")
        print("in another terminal first!")
        input("Press Enter when daemon is running...")
        mini = ReachyMini(localhost_only=True, media_backend="no_media")
        print("✅ Connected to simulator!")
        break
    else:
        print("❌ Invalid choice! Enter 1 or 2")

print()
print("Robot is ready to show emotions!")
print()
print("Press a key to show emotion:")
print("  h - Happy")
print("  s - Sad")
print("  e - Excited")
print("  c - Curious")
print("  q - Quit")
print()

# Emotion Functions
# Each function makes the robot express a different emotion

def show_happy():
    """Make the robot look happy!"""
    print("😊 Showing HAPPY emotion!")

    # Happy = looking up optimistically!
    # Pitch up (positive = looking up)
    head_pose = create_head_pose(
        roll=0,     # No side tilt
        pitch=15,   # Look up 15 degrees (in DEGREES!)
        yaw=0       # Looking straight ahead
    )

    # Move head and antennas together
    mini.goto_target(
        head=head_pose,      # Head looking up
        antennas=[0.8, 0.8], # Both antennas up high
        duration=0.5
    )
    time.sleep(0.5)
    print("   Done!")

def show_sad():
    """Make the robot look sad..."""
    print("😢 Showing SAD emotion...")

    # Sad = looking down dejectedly
    # Negative pitch = looking down
    head_pose = create_head_pose(
        roll=0,
        pitch=-20,  # Look DOWN 20 degrees (sad...)
        yaw=0
    )

    # Move slowly for a droopy, sad feeling
    mini.goto_target(
        head=head_pose,        # Head looking down
        antennas=[-0.8, -0.8], # Both antennas drooping down
        duration=0.8           # Slower movement = more sadness
    )
    time.sleep(0.8)
    print("   Done!")

def show_excited():
    """Make the robot look excited with fast wiggles!"""
    print("🤩 Showing EXCITED emotion!")

    # Excited = fast nodding + antenna wiggling!
    for i in range(3):  # Do this 3 times
        # Nod up
        head_up = create_head_pose(
            roll=0,
            pitch=10,  # Nod up (DEGREES!)
            yaw=0
        )
        mini.goto_target(
            head=head_up,
            antennas=[1.0, -1.0],  # Antennas opposite
            duration=0.2
        )
        time.sleep(0.2)

        # Nod down
        head_down = create_head_pose(
            roll=0,
            pitch=-10,  # Nod down (DEGREES!)
            yaw=0
        )
        mini.goto_target(
            head=head_down,
            antennas=[-1.0, 1.0],  # Swap antennas
            duration=0.2
        )
        time.sleep(0.2)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    mini.goto_target(
        head=neutral_head,
        antennas=[0, 0],
        duration=0.3
    )
    time.sleep(0.3)
    print("   Done!")

def show_curious():
    """Make the robot look curious - tilting and exploring!"""
    print("🤔 Showing CURIOUS emotion!")

    # Curious = head tilting side to side (like a confused puppy!)
    # Tilt right
    head_right = create_head_pose(
        roll=20,   # Tilt head RIGHT (DEGREES!)
        pitch=5,   # Slight upward look (questioning)
        yaw=0
    )
    mini.goto_target(
        head=head_right,
        antennas=[0.6, -0.3],  # One antenna up, curious!
        duration=0.6
    )
    time.sleep(0.6)

    # Tilt left
    head_left = create_head_pose(
        roll=-20,  # Tilt head LEFT (DEGREES!)
        pitch=5,
        yaw=0
    )
    mini.goto_target(
        head=head_left,
        antennas=[-0.3, 0.6],  # Swap antennas
        duration=0.6
    )
    time.sleep(0.6)

    # Tilt right again
    mini.goto_target(
        head=head_right,
        antennas=[0.6, -0.3],
        duration=0.6
    )
    time.sleep(0.6)

    # Return to neutral
    neutral_head = create_head_pose(0, 0, 0)
    mini.goto_target(
        head=neutral_head,
        antennas=[0, 0],
        duration=0.5
    )
    time.sleep(0.5)
    print("   Done!")

# Main program loop - wait for keyboard input
try:
    while True:
        # Ask the user to press a key
        user_input = input("Choose emotion (h/s/e/c/q): ").lower()

        # Call the right function based on what key was pressed
        if user_input == 'h':
            show_happy()
        elif user_input == 's':
            show_sad()
        elif user_input == 'e':
            show_excited()
        elif user_input == 'c':
            show_curious()
        elif user_input == 'q':
            print("\nGoodbye! 👋")
            print("Disconnecting robot...")
            # Force immediate exit, killing all threads
            os._exit(0)
        else:
            print("Invalid choice! Try h, s, e, c, or q")

        print()  # Empty line for readability

except KeyboardInterrupt:
    print("\nGoodbye!")
    print("Robot disconnected safely.")
