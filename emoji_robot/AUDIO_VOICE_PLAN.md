# Audio/Voice Features Plan for Emoji Robot

## Project Status
- **File Created:** `emoji_robot_audio_voice.py` (copied from emoji_robot_clean.py)
- **Date Started:** December 26, 2024
- **Date Completed:** December 26, 2025
- **Status:** ✅ ALL FEATURES IMPLEMENTED AND WORKING!

## Goal
Add audio and voice features to make the emoji robot more interactive and expressive.

## Features to Implement (Step-by-Step)

### Step 1: Text-to-Speech (Robot Speaks) 🗣️ ✅ COMPLETED
**What:** Robot says phrases for each emotion
- Happy: "I'm so happy!"
- Sad: "I feel sad..."
- Excited: "Wow, I'm excited!"
- Curious: "Hmm, curious..."

**Implementation:** ✅
- Used macOS `say` command to generate speech
- Converts AIFF → WAV using `ffmpeg`
- Plays through `robot.media.play_sound()` in simulator
- Works perfectly with Mac speakers during development

### Step 2: Sound Effects 🔊 ✅ COMPLETED
**What:** Play sound effects when showing emotions
- Happy: cheerful beep/melody
- Sad: low/descending tone
- Excited: rapid beeps
- Curious: questioning sound

**Implementation:** ✅
- Used built-in SDK sounds from robot's assets folder
- Happy: `wake_up.wav` (cheerful sound)
- Sad: `go_sleep.wav` (calm sound)
- Excited: `dance1.wav` (energetic sound)
- Curious: `confused1.wav` (questioning sound)
- Plays through `robot.media.play_sound()` - SDK automatically finds files

### Step 3: Voice Commands 🎤 ✅ COMPLETED
**What:** Trigger emotions by speaking
- Say "happy" → shows happy emotion
- Say "sad" → shows sad emotion
- Say "excited" → shows excited emotion
- Say "curious" → shows curious emotion

**Implementation:** ✅
- Used `speech_recognition` library with Google Speech Recognition API
- Used `pyaudio` to access Mac's microphone during development
- Continuous listening loop with keyword detection
- Supports quit commands: "quit", "stop", "exit"
- Works perfectly for development/testing on Mac

### Step 4: Full Integration 🎭 ✅ COMPLETED
**What:** Combine all features
- Voice command triggers emotion
- Robot shows physical emotion (head + antennas)
- Robot speaks phrase
- Robot plays sound effect

**Implementation:** ✅
**Example flow (all working!):**
1. User says "happy"
2. Robot detects voice command via speech recognition
3. Robot says "I'm so happy!" (TTS)
4. Robot plays cheerful sound (wake_up.wav)
5. Robot looks up with antennas raised (physical movement)

**Control Modes Available:**
- Keyboard control: Press h/s/e/c keys
- Voice control: Speak emotion names

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

## 🚨 IMPORTANT: Deployment to Robot Considerations

### Current Implementation (Mac Development)
The current code works perfectly for development on Mac with the simulator, but uses Mac-specific approaches:

**Audio Output (TTS & Sound Effects):**
- ✅ **Portable:** Uses `robot.media.play_sound()` - will work on robot!
- ✅ **Simulator:** Plays through Mac speakers
- ✅ **Real Robot:** Will play through robot's speakers automatically

**Audio Input (Voice Commands):**
- ⚠️ **Current:** Uses PyAudio to access Mac's microphone
- ⚠️ **Consideration:** Should use robot's ReSpeaker microphone array when deployed
- ⚠️ **Internet:** Requires internet for Google Speech Recognition API

### Required Changes for Production Robot App

When deploying as an app on the robot, consider these optimizations:

#### 1. Use Robot's Native Microphone Array
**Current (Mac development):**
```python
# Uses Mac's microphone via PyAudio
recognizer = sr.Recognizer()
microphone = sr.Microphone()
audio = recognizer.listen(source)
```

**Recommended for Robot:**
```python
# Use robot's ReSpeaker microphone array
robot.media.start_recording()
audio_samples = robot.media.get_audio_sample()  # 16kHz stereo
# Process audio_samples with speech_recognition
# Can also use robot.media.audio.get_DoA() for direction detection!
```

#### 2. Consider Offline Speech Recognition
**Current:** Google Speech Recognition (requires internet)

**Options for Robot:**
- **Vosk:** Offline, lightweight, good for keywords
- **Whisper:** More accurate, heavier
- **Keep Google API:** If robot has reliable internet

#### 3. TTS Adaptation
**Current:** macOS `say` command (Mac-specific)

**For Robot (Linux):**
- Replace `say` command with:
  - `espeak` or `espeak-ng` (lightweight, Linux TTS)
  - `pyttsx3` (cross-platform)
  - Or pre-generate speech files and include them in app package

### Deployment Checklist

When ready to build the production app:

- [ ] Replace PyAudio microphone with `robot.media` recording
- [ ] Choose offline speech recognition or ensure internet dependency is documented
- [ ] Replace macOS `say` with Linux-compatible TTS
- [ ] Test with robot's actual hardware (ReSpeaker microphone array)
- [ ] Consider using Direction of Arrival (DoA) feature for enhanced interaction
- [ ] Package TTS audio files or ensure TTS works on robot's Linux OS
- [ ] Update `requirements.txt` with correct dependencies for robot deployment
- [ ] Test full workflow on robot hardware before deploying via Hugging Face CLI

### Why Current Code Still Works

**The good news:** The current code is ~90% portable!
- ✅ All logic, emotion functions, keyword mapping: portable
- ✅ Speech_recognition library: works on Linux
- ✅ Sound playback via SDK: already robot-native
- ⚠️ Only needs: microphone input method + TTS adaptation

### Development Workflow

**Current (Perfect for now):**
1. Develop on Mac with simulator ✅
2. Test movements on real robot ✅
3. Voice commands work on Mac for development ✅

**Future (Production deployment):**
1. Adapt microphone input to use robot's ReSpeaker
2. Adapt TTS for Linux
3. Deploy app via Hugging Face CLI
4. Run natively on robot with full hardware integration

---

**Status:** Ready for deployment with minor adaptations documented above!
