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

### Feature 1: Emoji Robot Integration 🎭
**Status:** 🔄 In Progress

**Goal:** Robot shows emotions when detecting/losing faces

**Behaviors:**
- Show "curious" emotion when first detecting a face
- Show "happy" emotion when face stays in view
- Show "sad" emotion when person leaves (face disappears)
- Return to neutral after emotions

**Implementation:**
- Import emotion functions from emoji_robot
- Track face detection state (was_detected vs is_detected)
- Trigger emotions on state changes
- Add cooldown to prevent too many emotions

**Files:**
- Create: `face_tracking_with_emotions.py`
- Import from: `../emoji_robot/emoji_robot_clean.py`

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
- 🔄 Starting Feature 1: Emoji Robot Integration

---

## Next Session Tasks

**Current:** Feature 1 - Emoji Robot Integration
- [ ] Create face_tracking_with_emotions.py
- [ ] Import emotion functions from emoji_robot
- [ ] Implement state tracking (face appeared/disappeared)
- [ ] Add emotion triggers
- [ ] Test complete workflow
- [ ] Document behavior

---

**Last Updated:** December 26, 2025
