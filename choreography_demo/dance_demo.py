"""
Reachy Mini Dance Demo - Another One Bites The Dust

This script loads pre-built dance moves from the SDK and plays them
in sequence to create a choreographed dance routine!
"""

import os
import sys

# Set up library paths for GStreamer on macOS
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')
os.environ['GI_TYPELIB_PATH'] = '/opt/homebrew/lib/girepository-1.0'

from reachy_mini import ReachyMini
from reachy_mini.motion.recorded_move import RecordedMoves
import json
import time
import threading

print("🎵 Loading choreography: Another One Bites The Dust by Queen!")
print()

# Load the choreography file
with open("another_one_bites_the_dust.json", "r") as f:
    choreography = json.load(f)

print(f"Song BPM: {choreography['bpm']}")
print(f"Number of moves in sequence: {len(choreography['sequence'])}")
print()

# Connect to robot
print("Connecting to Reachy Mini...")
# Skip the complex WebRTC media backend - play music from Mac instead!
# This avoids GStreamer/libnice dependency issues
reachy = ReachyMini(localhost_only=False, media_backend="no_media")
has_audio = False
print("✅ Connected! Music will play from your Mac speakers.")

print("Loading dance moves library...")
print()

# Load the pre-built dance moves from the SDK
# The SDK downloads them from Hugging Face
dance_moves = RecordedMoves("pollen-robotics/reachy-mini-dances-library")
print(f"Available dance moves: {dance_moves.list_moves()}")
print()

# Function to play music
def play_music():
    """Play the 8-bit music file through robot or Mac speakers"""
    if has_audio:
        # Play through robot's speakers!
        try:
            print("🔊 Playing 8-bit music through ROBOT speakers! 🤖")
            reachy.media.play_sound("another_one_8bit.wav")
        except Exception as e:
            print(f"⚠️  Could not play through robot: {e}")
    else:
        # Fallback to Mac speakers
        try:
            import sounddevice as sd
            from scipy.io import wavfile
            print("🔊 Playing 8-bit music from your Mac...")
            sample_rate, audio_data = wavfile.read("another_one_8bit.wav")
            sd.play(audio_data, sample_rate)
            sd.wait()
        except Exception as e:
            print(f"⚠️  Could not play music: {e}")

# Play the choreography!
print("🎸 Starting the show! Press Ctrl+C to stop")
print()

try:
    # Start the music in a separate thread so dance can start immediately
    music_thread = threading.Thread(target=play_music)
    music_thread.start()

    time.sleep(0.5)  # Small delay to let music start
    for step in choreography['sequence']:
        move_name = step['move']
        cycles = step.get('cycles', 1)

        print(f"▶️  Playing: {move_name} ({cycles} cycles)")

        # Get the move from the library
        move = dance_moves.get(move_name)

        # Play it the specified number of times
        for i in range(cycles):
            reachy.play_move(move, initial_goto_duration=0.5)
            time.sleep(0.1)  # Small pause between cycles

        print(f"   ✓ Done!")
        print()

    print("🎉 Performance complete! The show must go on! 🎤")

except KeyboardInterrupt:
    print("\n\n⏸️  Show paused!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Make sure the dance moves library is available!")

print("Disconnecting...")
