"""
Reachy Mini Hello World Example

This script connects to your Reachy Mini robot and makes the antennas wiggle.
It's your first step into robotics programming!
"""

from reachy_mini import ReachyMini

# Connect to the robot using a context manager (automatically handles cleanup)
# localhost_only=False allows connection to the wireless robot
# media_backend="no_media" disables camera/audio (we don't need it for this simple demo)
with ReachyMini(localhost_only=False, media_backend="no_media") as mini:
    print("🤖 Connected to Reachy Mini!")

    print("👋 Wiggling antennas...")

    # Move antennas to the right
    mini.goto_target(antennas=[0.5, -0.5], duration=0.5)

    # Move antennas to the left
    mini.goto_target(antennas=[-0.5, 0.5], duration=0.5)

    # Return to center position
    mini.goto_target(antennas=[0, 0], duration=0.5)

    print("✅ Done! Your first Reachy Mini program worked!")
