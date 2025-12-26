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
**Status:** ✅ COMPLETED

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

**Files Created:**
✅ `face_tracking_with_emotions.py` - Emotions only (for learning)
✅ `face_tracking_with_emotions_and_speech.py` - Emotions + Speech (enhanced version)

**Completed:** December 26, 2025

---

### Feature 2: Greeting Behavior 👋
**Status:** ⏳ Pending

**Goal:** Robot waves antennas when seeing someone

**Behaviors:**
- Wiggle antennas when first detecting face
- Different antenna patterns for different scenarios
- Combine with curious emotion

**Implementation:**
- Add antenna wave function
- Trigger on new face detection
- Smooth antenna movements

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

**Current:** Feature 2 - Antenna Greeting Behavior
- [ ] Create face_tracking_with_greetings.py (or enhance existing)
- [ ] Add antenna wave function
- [ ] Trigger antenna greeting on new face detection
- [ ] Combine with curious emotion
- [ ] Test antenna patterns
- [ ] Document behavior

**Completed Today:**
- ✅ Feature 1: Emoji Robot Integration + Speech
  - ✅ Created face_tracking_with_emotions.py
  - ✅ Created face_tracking_with_emotions_and_speech.py
  - ✅ Imported emotion functions from emoji_robot
  - ✅ Implemented state machine for emotion management
  - ✅ Added speech synthesis with robot.media.play_sound()
  - ✅ Tested complete workflow with simulator
  - ✅ Committed to GitHub

---

**Last Updated:** December 26, 2025 (End of Session)
