"""
Emoji Robot - Express Emotions with Reachy Mini

A clean, well-structured program that lets you control your robot's emotions.
Press keys to trigger different emotional expressions!
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time
import os
import subprocess
from pathlib import Path
import requests


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

# Speech phrases for each emotion
SPEECH_PHRASES = {
    'happy': "I'm so happy!",
    'sad': "I feel sad...",
    'excited': "Wow, I'm excited!",
    'curious': "Hmm, curious..."
}

# Sound effects for each emotion (using built-in SDK sounds)
SOUND_EFFECTS = {
    'happy': "wake_up.wav",      # Upbeat, cheerful sound
    'sad': "go_sleep.wav",        # Slower, calmer sound
    'excited': "dance1.wav",      # Energetic dance sound
    'curious': "confused1.wav"    # Questioning, curious sound
}

# Temporary directory for generated speech files (in project folder)
TEMP_SPEECH_DIR = Path(__file__).parent / "temp_speech"

# Robot connection mode (will be set during initialization)
IS_REAL_ROBOT = False
ROBOT_URL = "http://reachy-mini.local:8000"


# ============================================================
# AUDIO HELPER FUNCTIONS
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
    aiff_file = TEMP_SPEECH_DIR / f"{emotion_name}.aiff"
    wav_file = TEMP_SPEECH_DIR / f"{emotion_name}.wav"

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


def play_speech(robot, emotion_name):
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

        if IS_REAL_ROBOT:
            # Use REST API for real robot (TODO: need to upload file first)
            print(f"   🔊 '{phrase}' (TTS on real robot not yet implemented)")
            # For now, skip TTS on real robot until we implement file upload
        else:
            # Play through Mac speakers in simulator
            robot.media.play_sound(str(speech_file))
            print(f"   🔊 '{phrase}'")

    except Exception as e:
        print(f"   ⚠️ Speech error: {e}")


def play_sound_via_api(sound_path):
    """
    Play a sound file on the real robot using REST API.

    Args:
        sound_path: Path to sound file (local or built-in SDK sound name)
    """
    try:
        # For built-in sounds, just pass the filename
        # For custom sounds, we'd need to upload first (TODO for later)
        url = f"{ROBOT_URL}/media/sound/play"

        # Try to play the sound via API
        # Note: This endpoint might not exist - need to check robot API
        response = requests.post(url, json={"sound": str(sound_path)}, timeout=5)

        if response.status_code == 200:
            return True
        else:
            print(f"   ⚠️ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️ REST API error: {e}")
        return False


def play_sound_effect(robot, emotion_name):
    """
    Play a sound effect for a given emotion using built-in SDK sounds.

    Args:
        robot: ReachyMini robot instance
        emotion_name: Name of the emotion (key in SOUND_EFFECTS)
    """
    try:
        # Get the sound file for this emotion
        sound_file = SOUND_EFFECTS[emotion_name]

        if IS_REAL_ROBOT:
            # Use REST API for real robot
            success = play_sound_via_api(sound_file)
            if success:
                print(f"   🎵 Sound: {sound_file} (via API)")
            else:
                print(f"   ⚠️ Could not play sound via API")
        else:
            # Use SDK media backend for simulator
            robot.media.play_sound(sound_file)
            print(f"   🎵 Sound: {sound_file}")

    except Exception as e:
        print(f"   ⚠️ Sound effect error: {e}")


# ============================================================
# EMOTION FUNCTIONS
# ============================================================

def show_happy(robot):
    """Express happiness - looking up with antennas raised."""
    print("😊 Showing HAPPY emotion!")

    # Play speech and sound effect
    play_speech(robot, 'happy')
    play_sound_effect(robot, 'happy')

    # Show physical emotion
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

    # Play speech and sound effect
    play_speech(robot, 'sad')
    play_sound_effect(robot, 'sad')

    # Show physical emotion
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

    # Play speech and sound effect
    play_speech(robot, 'excited')
    play_sound_effect(robot, 'excited')

    # Show physical emotion
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

    # Play speech and sound effect
    play_speech(robot, 'curious')
    play_sound_effect(robot, 'curious')

    # Show physical emotion
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
    global IS_REAL_ROBOT

    # Setup speech directory
    setup_speech_directory()

    print(BANNER)
    print("Choose mode:")
    print("  1 - Real Robot (wireless)")
    print("  2 - Simulation (no robot needed)")
    print()

    while True:
        mode = input("Enter 1 or 2: ").strip()

        if mode == "1":
            print("\n🤖 Connecting to REAL robot...")
            print("ℹ️  Using REST API for audio (bypasses WebRTC)")
            # Use no_media to avoid WebRTC - we'll use REST API for audio instead
            robot = ReachyMini(localhost_only=False, media_backend="no_media")
            IS_REAL_ROBOT = True
            print("✅ Connected to real robot!")
            return robot

        elif mode == "2":
            print("\n🎮 Starting SIMULATION...")
            print("(Make sure simulator daemon is running!)")
            input("Press Enter when ready...")
            # Use default_no_video to avoid video streaming buffer issues
            robot = ReachyMini(localhost_only=True, media_backend="default_no_video")
            IS_REAL_ROBOT = False
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
