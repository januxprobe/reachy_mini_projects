# Audio/Voice Features Plan for Emoji Robot

## Project Status
- **File Created:** `emoji_robot_audio_voice.py` (copied from emoji_robot_clean.py)
- **Date Started:** December 26, 2024
- **Status:** Ready to start implementation

## Goal
Add audio and voice features to make the emoji robot more interactive and expressive.

## Features to Implement (Step-by-Step)

### Step 1: Text-to-Speech (Robot Speaks) 🗣️
**What:** Robot says phrases for each emotion
- Happy: "I'm so happy!"
- Sad: "I feel sad..."
- Excited: "Wow, I'm excited!"
- Curious: "Hmm, curious..."

**Implementation approach:**
- Use Python's `pyttsx3` library for TTS
- OR use macOS `say` command
- OR pre-record audio files

### Step 2: Sound Effects 🔊
**What:** Play sound effects when showing emotions
- Happy: cheerful beep/melody
- Sad: low/descending tone
- Excited: rapid beeps
- Curious: questioning sound

**Implementation approach:**
- Generate simple tones using `numpy` and `scipy`
- OR use pre-made sound effect files
- Play through robot speakers or Mac speakers

### Step 3: Voice Commands 🎤
**What:** Trigger emotions by speaking
- Say "happy" → shows happy emotion
- Say "sad" → shows sad emotion
- Say "excited" → shows excited emotion
- Say "curious" → shows curious emotion

**Implementation approach:**
- Use Python's `speech_recognition` library
- Listen for keywords
- Map keywords to emotion functions

### Step 4: Full Integration 🎭
**What:** Combine all features
- Voice command triggers emotion
- Robot shows physical emotion (head + antennas)
- Robot speaks phrase
- Robot plays sound effect

**Example flow:**
1. User says "happy"
2. Robot detects voice command
3. Robot says "I'm so happy!"
4. Robot looks up with antennas raised
5. Robot plays cheerful sound

## Technical Notes

### Audio Capabilities (from SDK)
- `robot.media.play_sound("filename.wav")` - plays audio files
- Robot has speakers (but may have compatibility issues on macOS)
- Fallback: play through Mac speakers using `sounddevice`

### Libraries Needed
```bash
# Install when ready:
pip install pyttsx3           # Text-to-speech
pip install SpeechRecognition # Voice recognition
pip install pyaudio          # Audio input (for voice commands)
```

### Files Structure
```
emoji_robot/
├── emoji_robot_audio_voice.py  # Main program
├── sounds/                      # Folder for sound effects
│   ├── happy.wav
│   ├── sad.wav
│   ├── excited.wav
│   └── curious.wav
└── AUDIO_VOICE_PLAN.md         # This file
```

## Current Code Base
Starting from: `emoji_robot_clean.py`
- Clean structure with init_robot() and main()
- 4 emotion functions: show_happy(), show_sad(), show_excited(), show_curious()
- Dictionary dispatch for emotions
- Support for both real robot and simulator

## Next Session Tasks

### Immediate Next Steps:
1. Choose which feature to implement first (suggest: Step 1 - TTS)
2. Install required libraries
3. Test simple TTS with one emotion
4. Expand to all emotions
5. Move to next step

### Questions to Answer:
- [ ] Use robot speakers or Mac speakers? (Start with Mac for simplicity)
- [ ] Pre-recorded audio or generated speech?
- [ ] Simple or complex sound effects?

## Resources
- **Main README:** `~/Documents/Workspace/reachy_mini_projects/README.md`
- **SDK Docs:** https://github.com/pollen-robotics/reachy_mini
- **Current working directory:** `~/Documents/Workspace/reachy_mini_projects/emoji_robot/`

## Notes
- Keep `emoji_robot_clean.py` unchanged as reference
- Test features one at a time
- Use simulator for development (robot battery!)
- Remember: `reachy-sim` to start simulator, `reachy` to activate env

---

**Ready to continue:** Show this file and say "Let's continue with audio/voice features"
