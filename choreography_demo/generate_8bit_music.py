"""
Generate 8-bit style music for "Another One Bites The Dust"

Creates a retro chiptune version of the iconic bassline!
"""

import numpy as np
from scipy.io import wavfile

# Audio settings
SAMPLE_RATE = 44100  # Standard audio sample rate
BPM = 114  # From the choreography file
BEAT_DURATION = 60 / BPM  # Duration of one beat in seconds

def generate_square_wave(frequency, duration, volume=0.3):
    """Generate a square wave (classic 8-bit sound)"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Square wave is created by taking the sign of a sine wave
    wave = volume * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

def generate_silence(duration):
    """Generate silence"""
    return np.zeros(int(SAMPLE_RATE * duration))

def create_another_one_bites_the_dust():
    """
    Create the iconic bassline rhythm:
    "dum dum dum - dum dum dum dum - DUM DUM"

    Using notes from the E minor scale (8-bit style frequencies)
    """
    print("🎵 Generating 8-bit version of 'Another One Bites The Dust'...")

    # Musical notes (frequencies in Hz) - using lower octave for bass
    E2 = 82.41   # Low E (main note)
    A2 = 110.00  # A
    G2 = 98.00   # G

    # The iconic rhythm pattern (approximately 8 beats)
    song = np.array([])

    # Repeat the pattern 8 times (matches roughly 32 beats for the dance)
    for _ in range(8):
        # "dum dum dum" - three quick hits
        song = np.concatenate([song, generate_square_wave(E2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.1)])
        song = np.concatenate([song, generate_square_wave(E2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.1)])
        song = np.concatenate([song, generate_square_wave(E2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.6)])

        # "dum dum dum dum" - four more hits
        song = np.concatenate([song, generate_square_wave(E2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.1)])
        song = np.concatenate([song, generate_square_wave(G2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.1)])
        song = np.concatenate([song, generate_square_wave(A2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.1)])
        song = np.concatenate([song, generate_square_wave(E2, BEAT_DURATION * 0.4)])
        song = np.concatenate([song, generate_silence(BEAT_DURATION * 0.6)])

    # Normalize to prevent clipping
    song = np.clip(song, -1, 1)

    # Convert to 16-bit integer format
    audio_data = np.int16(song * 32767)

    # Save as WAV file
    wavfile.write("another_one_8bit.wav", SAMPLE_RATE, audio_data)
    print("✅ 8-bit music generated: another_one_8bit.wav")
    print(f"   Duration: {len(song) / SAMPLE_RATE:.1f} seconds")
    print(f"   BPM: {BPM}")

if __name__ == "__main__":
    create_another_one_bites_the_dust()
    print("\n🎮 Retro sound ready for your robot!")
