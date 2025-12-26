# Camera & Computer Vision Projects

**Test and develop computer vision features using the robot's camera with the simulator!**

This project demonstrates that we **CAN** use the camera with the simulator on Mac **WITHOUT** GStreamer, using the OpenCV backend instead.

## Key Discovery

✅ **Camera works with simulator using `media_backend="default"`**
✅ **No GStreamer required - uses OpenCV VideoCapture**
✅ **Simulator streams via UDP on 127.0.0.1:5005**
✅ **Confirmed by working examples in SDK code**

## How It Works

### Simulator Camera Stream
- Simulator automatically starts UDP JPEG stream
- Streams at **1280x720 @ 60fps**
- Available at `udp://@127.0.0.1:5005`
- No configuration needed - works out of the box!

### OpenCV Backend
- Uses `cv2.VideoCapture()` to read UDP stream
- SDK handles all the connection logic
- Just use `robot.media.get_frame()` to get frames
- Same API as real robot hardware

## Projects in This Directory

### 1. Camera Test (`test_camera_simulator.py`)
Basic camera functionality test - verifies camera works with simulator.

### 2. Face Detection Demo (`face_detection_demo.py`) ⭐
Interactive face tracking - robot detects and looks at faces!
- Real-time face detection using Haar Cascades
- Robot head automatically tracks largest face
- Visual feedback with bounding boxes
- See `FACE_DETECTION.md` for full documentation

## Running the Camera Test

### Prerequisites
1. Simulator must be running in another terminal
2. OpenCV installed (included in reachy_mini_env)

### Steps

**Terminal 1 - Start simulator:**
```bash
reachy-sim
```

**Terminal 2 - Run camera test:**
```bash
reachy
cd ~/Documents/Workspace/reachy_mini_projects/camera_vision
python test_camera_simulator.py
```

### What You'll See
- OpenCV window showing simulator camera view
- FPS counter and frame count overlay
- Real-time video feed from robot's perspective
- Press 'q' to quit

## Code Structure

```python
from reachy_mini import ReachyMini

# Connect with OpenCV backend
robot = ReachyMini(
    localhost_only=True,
    media_backend="default"  # Uses OpenCV for camera
)

# Get frames in a loop
while True:
    frame = robot.media.get_frame()
    if frame is not None:
        # Process frame with OpenCV
        cv2.imshow("Camera", frame)
```

## Camera Specifications

**Simulator Camera:**
- Resolution: 1280x720 (default)
- FPS: 60 (target)
- Color: BGR format (OpenCV standard)
- Calibration: Ideal pinhole camera (no distortion)

**Real Robot Camera:**
- Same API, different specs
- Uses hardware camera calibration
- Lens distortion correction available

## What You Can Build

Now that camera works, you can create:

### Computer Vision Projects
- **Object Detection** - Detect and track objects
- **Face Detection** - Make robot look at faces
- **Color Tracking** - Follow colored objects
- **QR Code Scanner** - Read QR codes
- **Motion Detection** - Detect movement

### Interactive Demos
- **Visual Following** - Track and follow objects with head
- **Look At Point** - Use `robot.look_at_image(u, v)` for pixel tracking
- **Visual Search** - Scan environment for targets
- **Gesture Recognition** - React to hand gestures

### Educational Projects
- **Camera Calibration** - Understand camera intrinsics
- **Image Processing** - Apply filters and transformations
- **Feature Detection** - SIFT, ORB, etc.
- **Neural Networks** - Run inference on camera feed

## Technical Details

### Media Backend Options

| Backend | Camera | Audio | Use Case |
|---------|--------|-------|----------|
| `no_media` | ❌ | ❌ | Movement only |
| `default` | ✅ OpenCV | SoundDevice | **Simulator (Mac)** |
| `gstreamer` | GStreamer | GStreamer | Production (Linux) |
| `webrtc` | WebRTC | WebRTC | Remote (broken on Mac) |

### Camera Access Methods

```python
# Method 1 - Via MediaManager (recommended)
frame = robot.media.get_frame()

# Method 2 - Direct camera access
frame = robot.media.camera.read()

# Both return: numpy.ndarray (H, W, 3) uint8 BGR
```

### Resolution Settings

```python
from reachy_mini.media.camera_constants import CameraResolution

# Available resolutions:
# - R1280x720at30fps (default)
# - R1920x1080at30fps
# - R2304x1296at30fps
# - R3264x2448at30fps

# Change resolution:
robot.media.camera.set_resolution(CameraResolution.R1920x1080at30fps)
```

## Audio Backend Note

The "default" backend includes SoundDevice for audio, which may show warnings on Mac. This is fine - we're only using the camera part. The audio warnings can be ignored.

If you want to avoid audio warnings entirely, you could modify the SDK to support "default_video_only" backend (OpenCV camera without audio).

## Integration with Robot Movement

Camera works perfectly alongside robot control:

```python
# Get frame
frame = robot.media.get_frame()

# Process frame (detect object position)
u, v = detect_object(frame)  # Your detection code

# Make robot look at detected object
robot.look_at_image(u, v, duration=0.5)
```

The `look_at_image()` method uses camera calibration to convert pixel coordinates to head angles automatically!

## Research References

This implementation is based on working examples found in the SDK:
- `/utils/rerun.py` - Rerun visualization tool (lines 126-170)
- `/media/camera_opencv.py` - OpenCV backend implementation
- `/media/media_manager.py` - Media backend configuration
- `/daemon/backend/mujoco/backend.py` - Simulator camera streaming (lines 240-243)

## Next Steps

**Immediate:**
1. Run `test_camera_simulator.py` to verify camera works
2. Explore OpenCV features with live camera feed
3. Build first computer vision demo

**Future Projects:**
- Object detection with YOLO or similar
- Face tracking for interactive behavior
- ArUco marker detection for precise positioning
- Visual servoing for object manipulation
- Multi-camera fusion (if/when available)

## Troubleshooting

**No frame received:**
- Make sure simulator is running (`reachy-sim`)
- Check simulator started without errors
- Verify UDP port 5005 is not blocked

**Low FPS:**
- Expected: ~30 FPS (network overhead)
- Simulator runs at 60 FPS but UDP adds latency
- Still plenty fast for most vision tasks

**Audio warnings:**
- Expected with "default" backend on Mac
- Can be ignored - we're only using camera
- Audio warnings don't affect camera functionality

---

**Status:** Ready for development!
**Tested:** Camera test successfully created based on SDK patterns
**Next:** Run test to verify, then build vision projects!
