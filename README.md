# Reachy Mini Development Guide

Complete guide for developing apps for your Reachy Mini robot on Apple Silicon MacBook.

## Table of Contents
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Running Programs](#running-programs)
- [Simulator Setup](#simulator-setup)
- [Projects](#projects)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Activate Environment
```bash
reachy
```
That's it! This alias activates your virtual environment from anywhere.

### Run a Program (Real Robot)
```bash
reachy
cd ~/Documents/Workspace/reachy_mini_projects/emoji_robot
python emoji_robot.py
```

### Run with Simulator ⭐ EASY MODE

**Terminal 1 - Start simulator:**
```bash
reachy-sim
```
That's it! The script handles everything automatically.

**Terminal 2 - Run your program:**
```bash
reachy
cd ~/Documents/Workspace/reachy_mini_projects/emoji_robot
python emoji_robot.py
```
Choose option 2 (Simulation)

#### Manual Method (if you want to understand what's happening)
**Terminal 1:**
```bash
reachy
cd ~/Documents/Workspace/reachy_mini
mjpython -m reachy_mini.daemon.app.main --sim
```

**Terminal 2:**
```bash
reachy
cd ~/Documents/Workspace/reachy_mini_projects/emoji_robot
python emoji_robot.py
```

---

## Environment Setup

### Directory Structure
```
~/Documents/Workspace/
├── reachy_mini/              # SDK installation & virtual environment
│   └── reachy_mini_env/      # Virtual environment
└── reachy_mini_projects/     # Your projects (this folder)
    ├── helloworld/           # Basic antenna wiggle demo
    ├── emoji_robot/          # Emotion expressions with voice
    ├── choreography_demo/    # Dance moves with music
    ├── turn_to_speaker/      # Direction of arrival (DoA) demo
    └── camera_vision/        # Computer vision & face tracking
```

### What's Installed
- **Python 3.12.11** (via uv)
- **Reachy Mini SDK 1.2.4**
- **MuJoCo** (for simulation)
- **Git LFS** (for large files)

### Convenient Aliases
Added to `~/.zshrc` for easy access:

**Activate environment:**
```bash
alias reachy="source ~/Documents/Workspace/reachy_mini/reachy_mini_env/bin/activate"
```

**Start simulator:**
```bash
alias reachy-sim="~/Documents/Workspace/reachy_mini/start_simulator.sh"
```

Use these from any directory! No need to remember long paths.

---

## Running Programs

### Connection Types

#### Real Robot (Wireless)
```python
mini = ReachyMini(localhost_only=False, media_backend="no_media")
```
- Robot accessible at: `http://reachy-mini.local:8000/`
- Uses mDNS for network discovery
- No media backend (avoids GStreamer issues)

#### Simulator
```python
mini = ReachyMini(localhost_only=True, media_backend="no_media")
```
- Connects to local daemon
- Requires daemon running with `--sim` flag

---

## Simulator Setup

### Why Use Simulator?
- Develop without physical robot
- Code during lunch at work
- Save battery life
- Test safely before running on hardware

### Starting the Simulator

**IMPORTANT:** On macOS, must use `mjpython` (not regular python)!

```bash
reachy
cd ~/Documents/Workspace/reachy_mini
mjpython -m reachy_mini.daemon.app.main --sim
```

### What You'll See
- MuJoCo visualization window opens
- 3D view of simulated robot
- Console shows: `INFO: Started server process`

### Simulator Fixed Issues

**Problem:** `mjpython` couldn't find Python library
**Solution:** Created symlink:
```bash
ln -sf ~/.local/share/uv/python/cpython-3.12.11-macos-aarch64-none/lib/libpython3.12.dylib \
  ~/Documents/Workspace/reachy_mini/reachy_mini_env/lib/libpython3.12.dylib
```

This is already done - no need to run again!

---

## Projects

### 1. Hello World (`helloworld/`)
**What it does:** Makes antennas wiggle
**Run it:**
```bash
cd ~/Documents/Workspace/reachy_mini_projects/helloworld
python hello.py
```

**Key concepts:**
- Basic connection
- `goto_target()` for movement
- Antenna control with values -1.0 to 1.0

---

### 2. Emoji Robot (`emoji_robot/`)
**What it does:** Interactive emotion expressions

**Three versions available:**

#### Original Version (`emoji_robot.py`)
```bash
python emoji_robot.py
```
- Working code, gets the job done
- Good for understanding basics
- Shows how code evolves

#### Clean Version (`emoji_robot_clean.py`)
```bash
python emoji_robot_clean.py
```
- Professionally structured
- Uses best practices
- Easier to maintain and extend

#### Audio/Voice Version (`emoji_robot_audio_voice.py`) ⭐ NEW!
```bash
python emoji_robot_audio_voice.py
```
- **Text-to-Speech**: Robot speaks phrases for each emotion
- **Sound Effects**: Plays built-in SDK sounds
- **Full Integration**: Speech + sound + movement combined
- Uses Reachy Mini's native audio APIs
- Works with both simulator (Mac speakers) and real robot

**Features:**
- Choose real robot or simulator at startup
- 4 emotions: Happy, Sad, Excited, Curious
- Head movements + antenna expressions
- **NEW:** Voice output with TTS
- **NEW:** Sound effects using SDK built-in sounds

**Controls:**
- `h` - Happy: "I'm so happy!" + wake_up sound + looks up
- `s` - Sad: "I feel sad..." + go_sleep sound + looks down
- `e` - Excited: "Wow, I'm excited!" + dance sound + fast nodding
- `c` - Curious: "Hmm, curious..." + confused sound + head tilts
- `q` - Quit

**Key concepts:**
- `create_head_pose(roll, pitch, yaw)` - **uses DEGREES by default!**
- Roll = tilt sideways (±20°)
- Pitch = nod up/down (±20°)
- Yaw = turn left/right
- Combining head + antenna movements

**Code Structure Comparison:**

**Original (emoji_robot.py):**
```python
# Global variable
mini = ReachyMini(...)

def show_happy():
    # Uses global 'mini'
    mini.goto_target(...)

# Big if/elif chain
if user_input == 'h':
    show_happy()
elif user_input == 's':
    show_sad()
# ...
```

**Clean (emoji_robot_clean.py):**
```python
# Proper initialization
def init_robot():
    return ReachyMini(...)

def show_happy(robot):
    # Takes robot as parameter
    robot.goto_target(...)

# Dictionary dispatch pattern
emotions = {'h': show_happy, 's': show_sad}
if user_input in emotions:
    emotions[user_input](robot)
```

**What makes the clean version better?**
1. **Constants at top** - easy to modify
2. **Functions take parameters** - no globals, testable
3. **init_robot()** - separate initialization
4. **main()** - clear entry point
5. **Dictionary dispatch** - elegant key→function mapping
6. **Docstrings** - self-documenting code
7. **Entry guard** - `if __name__ == "__main__"`

**Code example:**
```python
from reachy_mini.utils import create_head_pose

# Happy - looking up
# Note: create_head_pose() expects DEGREES by default!
head_pose = create_head_pose(
    roll=0,      # No tilt
    pitch=15,    # Look UP 15 degrees (NOT radians!)
    yaw=0        # Straight ahead
)
robot.goto_target(
    head=head_pose,
    antennas=[0.8, 0.8],
    duration=0.5
)
```

#### Audio/Voice Implementation Details

**Text-to-Speech System:**
```python
# Uses macOS 'say' command to generate speech
# Converts AIFF to WAV for robot compatibility
def generate_speech(text, emotion_name):
    aiff_file = TEMP_SPEECH_DIR / f"{emotion_name}.aiff"
    wav_file = TEMP_SPEECH_DIR / f"{emotion_name}.wav"

    # Generate with macOS say
    subprocess.run(['say', '-o', str(aiff_file), text])

    # Convert to WAV using ffmpeg
    subprocess.run(['ffmpeg', '-i', str(aiff_file), '-y', str(wav_file)])

    return wav_file

# Play through robot
robot.media.play_sound(str(wav_file))
```

**Sound Effects Mapping:**
```python
SOUND_EFFECTS = {
    'happy': "wake_up.wav",      # Built-in SDK sound
    'sad': "go_sleep.wav",        # Built-in SDK sound
    'excited': "dance1.wav",      # Built-in SDK sound
    'curious': "confused1.wav"    # Built-in SDK sound
}

# Play sound effect
robot.media.play_sound(SOUND_EFFECTS['happy'])
```

**Media Backend Configuration:**
```python
# For audio features, use 'default' or 'default_no_video' backend
robot = ReachyMini(localhost_only=True, media_backend="default_no_video")

# Simulator uses Mac speakers/microphone as fallback
# Real robot uses built-in Reachy Mini Audio hardware
```

**Requirements:**
- macOS `say` command (built-in)
- `ffmpeg` for audio conversion: `brew install ffmpeg`
- Temp files stored in: `emoji_robot/temp_speech/`

---

### 3. Dance Demo (`choreography_demo/`)
**What it does:** Robot dances to 8-bit "Another One Bites The Dust"
**Run it:**
```bash
cd ~/Documents/Workspace/reachy_mini_projects/choreography_demo
python dance_demo.py
```

**Features:**
- Loads pre-built dance moves from SDK
- Plays 8-bit music from Mac speakers
- Choreographed sequence

**Key concepts:**
- `RecordedMoves` - library of pre-made movements
- `reachy.play_move()` - play recorded choreographies
- Threading for simultaneous music + dance
- Hugging Face datasets for moves

**Available move libraries:**
```python
from reachy_mini.motion.recorded_move import RecordedMoves

# Dance moves
dance_moves = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# Emotion moves
emotion_moves = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
```

---

### 4. Turn To Speaker (`turn_to_speaker/`) ⭐ NEW!
**What it does:** Robot turns its head toward you when you speak
**Run it:**
```bash
cd ~/Documents/Workspace/reachy_mini_projects/turn_to_speaker
python doa_demo.py
```

**Features:**
- Uses ReSpeaker 4-microphone array for sound localization
- Detects direction of sound (0-360°)
- Automatically turns head to face speaker
- Real-time speech detection
- Visual console feedback with direction indicators

**⚠️ Real Robot Only!**
- Requires physical ReSpeaker microphone array
- Cannot run in simulator (no hardware)

**Key concepts:**
- `robot.media.audio.get_DoA()` - Direction of Arrival sensor
- Returns: `{'angle': 45, 'is_speaking': True}`
- Coordinate conversion: DoA angle (0-360°) → robot yaw (±30°)
- Continuous monitoring loop with head tracking

**How it works:**
1. Monitors microphone array at 10Hz
2. Detects when speech occurs
3. Calculates direction angle
4. Converts to robot yaw coordinate system
5. Turns head smoothly toward speaker

**Example output:**
```
🗣️ SPEAKING | DoA: 045° | FRONT-RIGHT    ↗ | Yaw: +15.0°
   → Turning head to +15.0°

🔇 Quiet    | DoA: 270° | LEFT            ← | Yaw: -30.0°
```

---

### 5. Camera & Computer Vision (`camera_vision/`) ⭐ COMPLETE!
**What it does:** Interactive robot with face tracking, emotions, speech, and expressive antenna gestures

**Available Programs:**

#### Face Tracking with Greetings (`face_tracking_with_emotions_and_speech.py`)
```bash
cd ~/Documents/Workspace/reachy_mini_projects/camera_vision

# With display window (shows camera feed)
python face_tracking_with_emotions_and_speech.py

# Headless mode (better performance, no display)
python face_tracking_with_emotions_and_speech.py --headless
```

**✅ Implemented Features:**
- **Feature 1:** Face detection with emotions and speech
- **Feature 2:** Expressive antenna behaviors for all emotions

**Complete Interaction Sequences:**
1. **CURIOUS** (First Detection):
   - 👋 Wave antennas in alternating pattern
   - 🔊 Say "Hello! Who are you?"
   - 🤔 Show curious emotion (head tilt)

2. **HAPPY** (Person Stays 3+ Seconds):
   - 😊 Bounce antennas excitedly
   - 🔊 Say "I'm so happy to see you!"
   - 😊 Show happy emotion (look up)

3. **SAD** (Person Leaves):
   - 🔊 Say "Goodbye! Come back soon!"
   - 😢 Droop antennas slowly
   - 😢 Show sad emotion (look down)

**Key Features:**
- Real-time face detection with OpenCV Haar Cascades (20-30 FPS)
- Head tracking follows largest face
- Emotion state machine with 5-second cooldown
- Text-to-speech using macOS `say` + ffmpeg
- Three expressive antenna behaviors with consistent naming
- Headless mode for better performance

**⏸️ Deferred Features:**
- Face Recognition (Feature 3) - Heavy dependencies, deferred
- Emotion Detection (Feature 4) - ML models, deferred
- Multi-Person Tracking (Feature 5) - Future consideration

**Decision:** Deferred advanced features to validate existing ones on real robot hardware first. Focus on lightweight OpenCV-based features that work well without heavy ML dependencies.

**Technical:**
```python
# Face detection
robot = ReachyMini(localhost_only=True, media_backend="default_no_video")
webcam = cv2.VideoCapture(0)  # Uses Mac webcam for development
faces = face_cascade.detectMultiScale(gray)

# Antenna behaviors (consistent naming: antennas_<emotion>_<action>)
antennas_curious_wave(robot)   # Alternating wave greeting
antennas_happy_bounce(robot)   # Excited synchronized bouncing
antennas_sad_droop(robot)      # Slow wilting motion

# Speech synthesis
generate_speech("Hello! Who are you?", "curious")
robot.media.play_sound(wav_file)
```

**See Also:**
- Full documentation: `camera_vision/README.md`
- Enhancement plan: `camera_vision/ENHANCEMENT_PLAN.md`
- Face detection details: `camera_vision/FACE_DETECTION.md`

---

## Troubleshooting

### Simulator Issues on macOS

**Problem:** `Library not loaded: libpython3.12.dylib`
**Solution:** Symlink already created (see Simulator Setup section)

**Problem:** `No module named reachy_mini.daemon`
**Solution:** Use full module path:
```bash
mjpython -m reachy_mini.daemon.app.main --sim
```

**Problem:** GStreamer errors
**Solution:** Use `media_backend="no_media"` to bypass

---

### Connection Issues

**Can't connect to robot:**
1. Check robot is powered on
2. Verify same WiFi network
3. Test dashboard: `http://reachy-mini.local:8000/`
4. Confirm IP hasn't changed

**Timeout errors:**
- Robot daemon not running
- Network connectivity issue
- Wrong `localhost_only` setting

---

### Cursor IDE Setup

**⚠️ IMPORTANT: Do this for EVERY new project!**

Each project needs `.vscode/settings.json` for proper Python environment detection:
```json
{
  "python.defaultInterpreterPath": "/Users/jan.moons/Documents/Workspace/reachy_mini/reachy_mini_env/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.analysis.extraPaths": [
    "/Users/jan.moons/Documents/Workspace/reachy_mini/reachy_mini_env/lib/python3.12/site-packages"
  ],
  "cursorpyright.analysis.extraPaths": [
    "/Users/jan.moons/Documents/Workspace/reachy_mini/reachy_mini_env/lib/python3.12/site-packages"
  ]
}
```

**For new projects - Standard Setup:**
```bash
# After creating a new project directory:
cd ~/Documents/Workspace/reachy_mini_projects
cp -r emoji_robot/.vscode new_project_name/
```

This ensures:
- ✅ Cursor finds the correct Python interpreter
- ✅ Autocomplete works with reachy_mini SDK
- ✅ Type checking and linting work properly
- ✅ Integrated terminal activates environment automatically

---

## Robot Control Reference

### Antenna Control
```python
# Values: -1.0 (down) to 1.0 (up)
mini.goto_target(antennas=[0.8, 0.8], duration=0.5)  # Both up
mini.goto_target(antennas=[-0.8, -0.8], duration=0.5) # Both down
mini.goto_target(antennas=[1.0, -1.0], duration=0.5)  # Opposite
```

### Head Control
```python
from reachy_mini.utils import create_head_pose

# All angles in DEGREES (not radians!)
head = create_head_pose(
    roll=20,    # Tilt sideways: + = right, - = left (degrees)
    pitch=15,   # Nod: + = up, - = down (degrees)
    yaw=-30     # Turn: + = right, - = left (degrees)
)
mini.goto_target(head=head, duration=1.0)
```

### Combined Movement
```python
# Move head and antennas together
mini.goto_target(
    head=head_pose,
    antennas=[0.5, -0.5],
    duration=0.5
)
```

### Movement Speed
```python
duration=0.2  # Fast
duration=0.5  # Normal
duration=1.0  # Slow
```

---

## Tips & Best Practices

### Development Workflow
1. **Test in simulator first** - safer, faster iteration
2. **Use small duration values** - see movements clearly
3. **Add time.sleep()** - let movements complete
4. **Return to neutral** - reset position after emotions

### Code Organization
```python
# Good - separate functions for each behavior
def show_happy(robot):
    head = create_head_pose(roll=0, pitch=15, yaw=0)  # Degrees!
    robot.goto_target(head=head, antennas=[0.8, 0.8], duration=0.5)

# Bad - everything in one long script
```

### Safe Movements
- Keep antenna values between -1.0 and 1.0
- Use reasonable head angles (±30 degrees is safe)
- Test new moves in simulator first
- Add `time.sleep()` between rapid movements

---

## Useful Links

- **SDK Documentation:** [GitHub - Reachy Mini](https://github.com/pollen-robotics/reachy_mini)
- **Python SDK Guide:** [SDK Documentation](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/python-sdk.md)
- **Examples:** [Examples Folder](https://github.com/pollen-robotics/reachy_mini/tree/develop/examples)
- **Dashboard:** http://reachy-mini.local:8000/ (when robot connected)

---

## Lessons Learned

### Common Mistakes & Solutions

**1. Head movements not working (SOLVED!)**
- **Problem:** Used `math.radians()` to convert degrees
- **Cause:** `create_head_pose()` expects DEGREES by default (not radians!)
- **Solution:** Pass degrees directly: `pitch=15` not `pitch=math.radians(15)`

**2. Program hangs on quit (SOLVED!)**
- **Problem:** Background threads keep running
- **Cause:** SDK runs daemon threads that don't auto-stop
- **Solution:** Use `os._exit(0)` instead of `exit()` or `sys.exit()`

**3. Simulator won't start on macOS (SOLVED!)**
- **Problem:** `mjpython` can't find Python library
- **Cause:** uv installs Python in non-standard location
- **Solution:** Created symlink to lib directory (already done!)
- **Command:** `mjpython -m reachy_mini.daemon.app.main --sim`

**4. GStreamer/WebRTC errors (SOLVED!)**
- **Problem:** Media backend requires complex dependencies
- **Cause:** WebRTC needs libnice and other libraries
- **Solution:** Use `media_backend="no_media"` to bypass

**5. Audio buffer overrun warnings (SOLVED!)**
- **Problem:** UDP circular buffer overrun warnings in simulator
- **Cause:** Video streaming fills buffer faster than it's consumed
- **Solution:** Use `media_backend="default_no_video"` for audio-only features

**6. macOS 'say' command audio format (SOLVED!)**
- **Problem:** Robot's `play_sound()` failed with macOS-generated speech
- **Cause:** macOS `say` outputs AIFF format, robot expects WAV
- **Solution:** Convert AIFF → WAV using `ffmpeg` before playing

### Code Evolution

Watch how code improves from working → clean → featured:
1. **Start:** Get it working (emoji_robot.py)
2. **Refactor:** Make it clean (emoji_robot_clean.py)
3. **Enhance:** Add features (emoji_robot_audio_voice.py)
4. **Learn:** Compare all versions to understand why

---

## Project Status & Next Steps

### ✅ Completed Projects
1. **Hello World** - Basic antenna control
2. **Emoji Robot** - Emotions with voice and sound effects
3. **Dance Demo** - Choreographed dance with music
4. **Turn to Speaker** - Direction of arrival tracking
5. **Camera Vision** - Face tracking with emotions, speech, and antenna gestures
   - Feature 1: Face detection with emotions and speech
   - Feature 2: Expressive antenna behaviors for all emotions

### 🎯 Current Focus: Real Robot Deployment
**Priority:** Test and validate completed features on real Reachy robot hardware before adding complexity

**Why:** Ensure existing features work well in practice before pursuing advanced features that may have:
- Heavy computational requirements
- Complex dependencies not easily installed on robot
- Performance concerns on robot's hardware

### ⏸️ Deferred Features (Post Real Robot Validation)
- **Face Recognition** - Requires dlib/face_recognition (heavy dependencies)
- **Emotion Detection** - Requires ML models
- **Multi-Person Tracking** - Complex state management

### 💡 Future Enhancement Ideas
- **Combine DoA + Face Tracking** - Turn toward speaker and track face
- **Interactive Conversations** - Speech recognition + TTS responses
- **Follow the Speaker** - Track and follow person using DoA + vision
- **Voice-Controlled Games** - Interactive voice games
- **Custom Choreography** - Record and play custom dance sequences
- **AI/LLM Integration** - Natural conversation capabilities

### 🔍 Alternative Approaches to Consider
- **Lightweight Computer Vision** - Continue with OpenCV-based features
- **Cloud-Based Recognition** - Offload heavy processing to cloud services
- **ArUco Markers** - Precise positioning without heavy ML
- **Color/Motion Tracking** - Simple but effective tracking methods

---

## Summary

This repository contains a complete suite of interactive demos for Reachy Mini, progressing from basic control to advanced computer vision:

1. **Basic Movement** - Antenna and head control fundamentals
2. **Emotions** - Expressive behaviors with voice and sound
3. **Audio** - Speech synthesis, sound effects, and voice commands
4. **Spatial Awareness** - Direction of arrival tracking
5. **Computer Vision** - Face tracking with personalized interactions

**Development Strategy:** Build iteratively, test thoroughly in simulator, validate on real hardware before adding complexity.

---

*Last updated: January 7, 2026*
*Reachy Mini SDK Version: 1.2.4*
*Status: Camera vision features complete, ready for real robot deployment*
