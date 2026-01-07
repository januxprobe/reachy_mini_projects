# Camera Vision Enhancement Plan

**Started:** December 26, 2025
**Status:** In Progress

## Goal
Enhance the face detection demo with interactive behaviors, making the robot more expressive and engaging.

## Current Status ✅

**Working:**
- ✅ Face detection with OpenCV Haar Cascades
- ✅ Robot head tracking (follows largest face)
- ✅ Webcam integration for Mac development
- ✅ Real-time performance (20-30 FPS)

**Project:** `face_detection_webcam.py`

## Enhancement Features (Step-by-Step)

### Feature 1: Emoji Robot Integration + Speech 🎭🔊
**Status:** ✅ COMPLETED & TESTED

**Goal:** Robot shows emotions and speaks when detecting/losing faces

**Behaviors:**
- Show "curious" emotion + say "Hello! Who are you?" when first detecting face
- Show "happy" emotion + say "I'm so happy to see you!" when person stays (3+ seconds)
- Show "sad" emotion + say "Goodbye! Come back soon!" when person leaves (2+ seconds)
- Return to neutral after emotions

**Implementation:**
✅ Import emotion functions from emoji_robot
✅ Track face detection state (was_detected vs is_detected)
✅ Trigger emotions on state changes
✅ Add cooldown to prevent too many emotions (5 second minimum)
✅ State machine for emotion management
✅ Text-to-speech using macOS 'say' + ffmpeg
✅ Audio playback via robot.media.play_sound()
✅ Speech files cached in temp_speech/ directory
✅ Headless mode for better performance (--headless flag)

**Files Created:**
✅ `face_tracking_with_emotions.py` - Emotions only (for learning)
✅ `face_tracking_with_emotions_and_speech.py` - Emotions + Speech (enhanced version)

**Testing Results (January 7, 2026):**
✅ Face detection and tracking working
✅ All emotion triggers functioning correctly
✅ Speech synthesis and playback working
✅ Bug fixed: Timer initialization moved before cooldown check
✅ Performance: Headless mode significantly reduces system load

**Usage:**
```bash
# With display window (shows camera feed)
python face_tracking_with_emotions_and_speech.py

# Headless mode (better performance, no window)
python face_tracking_with_emotions_and_speech.py --headless
```

**Completed:** December 26, 2025
**Tested:** January 7, 2026

---

### Feature 2: Antenna Behaviors for All Emotions 👋
**Status:** ✅ COMPLETED

**Goal:** Robot uses expressive antenna gestures for all emotions

**Behaviors:**
- **CURIOUS:** Waves antennas in friendly greeting pattern (alternating wave)
- **HAPPY:** Bounces antennas excitedly (synchronized bouncing)
- **SAD:** Droops antennas slowly (wilting motion)

**Implementation:**
✅ Created `antennas_curious_wave()` function - alternating wave for greeting
✅ Created `antennas_happy_bounce()` function - excited bouncing motion
✅ Created `antennas_sad_droop()` function - slow wilting motion
✅ Integrated all antenna behaviors with emotion state machine
✅ Each emotion now has complete sequence: antenna gesture → speech → emotion display
✅ Consistent naming pattern: `antennas_<emotion>_<action>()`

**Behavior Flows:**

**CURIOUS (First Detection):**
1. 👋 Wave antennas (3 alternating waves, ~0.9 seconds)
2. 🔊 Say "Hello! Who are you?"
3. 🤔 Show curious emotion (head tilt)

**HAPPY (Person Stays 3+ Seconds):**
1. 😊 Bounce antennas (3 excited bounces, ~1.2 seconds)
2. 🔊 Say "I'm so happy to see you!"
3. 😊 Show happy emotion (look up, antennas raised)

**SAD (Person Leaves):**
1. 🔊 Say "Goodbye! Come back soon!"
2. 😢 Droop antennas slowly (wilting motion, ~1.5 seconds)
3. 😢 Show sad emotion (look down, antennas droopy)

**Completed:** January 7, 2026

---

### Feature 3: Face Recognition 🔍
**Status:** ⏳ Pending

**Goal:** Recognize specific people and respond differently

**Behaviors:**
- "Hello, Jan!" for known person
- "Who are you?" for unknown person
- Different emotions for different people

**Technical:**
- Use `face_recognition` library
- Store known face encodings
- Compare detected faces to known faces
- Add person-specific responses

**Requirements:**
```bash
pip install face_recognition
```

---

### Feature 4: Emotion Detection 😊
**Status:** ⏳ Pending

**Goal:** Detect if person is smiling and respond

**Behaviors:**
- Show happy emotion when person smiles
- Mirror person's expression
- Playful interaction

**Technical:**
- Use OpenCV smile detection cascade
- Or use deep learning model (DeepFace)
- Classify facial expressions
- Robot responds with matching emotion

---

### Feature 5: Multi-Person Tracking 👥
**Status:** ⏳ Pending

**Goal:** Track multiple people with priorities

**Behaviors:**
- Detect all faces
- Prioritize closest/largest
- Switch attention between people
- Greet new arrivals

**Technical:**
- Track all detected faces
- Assign IDs to faces
- Implement attention switching logic
- Remember who was already greeted

---

## Technical Notes

### Project Structure
```
camera_vision/
├── test_camera_simulator.py       # Basic camera test
├── face_detection_demo.py          # Original demo (robot camera)
├── face_detection_webcam.py        # Working demo (webcam)
├── face_tracking_with_emotions.py  # Feature 1 (NEW)
├── face_recognition_demo.py        # Feature 3 (FUTURE)
├── emotion_detection_demo.py       # Feature 4 (FUTURE)
└── multi_person_tracking.py        # Feature 5 (FUTURE)
```

### Dependencies
Current:
- reachy_mini SDK
- OpenCV (cv2)
- numpy

Future:
- face_recognition (for Feature 3)
- deepface (for Feature 4, optional)
- dlib (for face landmarks)

### Integration Points

**With emoji_robot:**
- Import emotion functions: `show_happy()`, `show_sad()`, `show_curious()`
- Use same robot instance
- Combine movement + emotions

**With turn_to_speaker (future):**
- Combine face tracking with sound direction
- Look at speaker when they talk
- Look at face when silent

---

## Development Workflow

**For each feature:**
1. Create new Python file (copy from face_detection_webcam.py)
2. Add new behavior logic
3. Test in simulator with webcam
4. Document in README
5. Commit to GitHub
6. Move to next feature

**Testing:**
- Use simulator for robot movements
- Use Mac webcam for face detection
- Verify emotions display correctly
- Check performance (maintain 20+ FPS)

---

## Decisions Log

**January 7, 2026:**
- ✅ Added headless mode to reduce system load from OpenCV display window
- ✅ Fixed bug: Timer initialization now happens before cooldown check
- ✅ Tested Feature 1 completely - all behaviors working as expected
- ✅ Headless mode uses --headless flag, controlled via argparse
- ✅ Implemented Feature 2: Antenna behaviors for all emotions
- ✅ Created three antenna gesture functions (greeting wave, happy bounce, sad droop)
- ✅ Integrated antenna behaviors with complete emotion sequences
- ✅ CURIOUS: alternating wave, HAPPY: excited bounce, SAD: slow droop

**December 26, 2025:**
- ✅ Use webcam for face detection (not simulator camera)
- ✅ Lower tracking threshold to 5 pixels for better responsiveness
- ✅ Use python3 for camera permissions on macOS
- ✅ Feature 1: Completed with emotions AND speech integration
- ✅ Use robot.media.play_sound() instead of afplay for consistency
- ✅ Changed media_backend to "default_no_video" for audio support
- ✅ Created two versions for progressive learning
- ✅ Verified SDK usage throughout codebase

---

## Next Session Tasks

**Current:** Feature 3 - Face Recognition
- [ ] Install face_recognition library
- [ ] Create face encoding storage system
- [ ] Implement person-specific responses
- [ ] Build training/enrollment workflow
- [ ] Test recognition accuracy

**Previous Sessions:**
- ✅ Feature 1: Emoji Robot Integration + Speech (December 26, 2025)
  - ✅ Created face_tracking_with_emotions.py
  - ✅ Created face_tracking_with_emotions_and_speech.py
  - ✅ Imported emotion functions from emoji_robot
  - ✅ Implemented state machine for emotion management
  - ✅ Added speech synthesis with robot.media.play_sound()
  - ✅ Committed to GitHub

**Today's Session (January 7, 2026):**
- ✅ Tested Feature 1 with simulator and webcam
- ✅ Fixed bug in emotion state machine timer initialization
- ✅ Added headless mode for better performance
- ✅ Documented headless mode option
- ✅ Verified all emotion triggers working correctly
- ✅ Implemented Feature 2: Antenna behaviors for all emotions
- ✅ Created antennas_curious_wave() - alternating wave for CURIOUS
- ✅ Created antennas_happy_bounce() - excited bouncing for HAPPY
- ✅ Created antennas_sad_droop() - wilting motion for SAD
- ✅ Standardized naming pattern: antennas_<emotion>_<action>()
- ✅ Integrated antenna behaviors with all three emotions
- ✅ Complete expressive sequences for each emotion

---

**Last Updated:** January 7, 2026
