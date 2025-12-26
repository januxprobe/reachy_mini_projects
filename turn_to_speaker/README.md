# Direction of Arrival (DoA) Demo

**Make the robot turn toward you when you speak!**

This demo showcases the ReSpeaker microphone array's Direction of Arrival (DoA) feature. The robot will detect when someone is speaking and automatically turn its head toward the sound source.

## What is DoA?

Direction of Arrival uses the ReSpeaker's 4-microphone circular array to:
- Detect the direction sound is coming from (0-360°)
- Detect when speech is occurring
- Calculate precise angles based on time-delay differences between microphones

## Features

- **Speech Detection**: Knows when someone is speaking vs. background noise
- **360° Sound Localization**: Detects sound from any direction around the robot
- **Automatic Head Tracking**: Robot turns to face the speaker
- **Real-time Monitoring**: Continuously updates as you move around
- **Visual Feedback**: Console displays direction, angle, and speech status

## Requirements

**⚠️ IMPORTANT: Robot Deployment Required!**

This demo requires:
- Physical Reachy Mini robot with ReSpeaker microphone array
- Code must run **ON the robot** (not remotely from Mac)
- Cannot run in simulator (no microphone array hardware)

### Mac Development Limitation

Due to WebRTC/GStreamer issues on macOS, the DoA feature **cannot be tested remotely** from your Mac. This is the same limitation we encountered with the audio/voice features.

**Why?**
- DoA requires media backend for ReSpeaker access
- Remote connection uses WebRTC for media streaming
- WebRTC has missing dependencies on Mac (libnice)

**Solution:**
- Develop and test movement logic on Mac
- Deploy complete app to robot via Hugging Face CLI
- Test full DoA functionality on robot itself

## How to Run

### For Development (Mac - Testing Logic Only)

You can review and develop the code on your Mac, but DoA won't work due to WebRTC limitations.

```bash
reachy
cd ~/Documents/Workspace/reachy_mini_projects/doa_demo
python doa_demo.py  # Will error at DoA access - expected!
```

### For Production (Deploy to Robot)

**Once you're ready to test the full DoA functionality:**

1. **Deploy app to robot via Hugging Face CLI:**
   ```bash
   # (Instructions coming - based on Hugging Face app deployment docs)
   # huggingface-cli login
   # Deploy doa_demo to robot
   ```

2. **Run on robot:**
   - Access robot's terminal or dashboard
   - Launch the deployed DoA app
   - Full DoA functionality will work!

3. **Test DoA:**
   - Walk around the robot while speaking
   - Robot will turn its head to face you
   - Console shows real-time DoA data

4. **Press Ctrl+C to stop**

## How It Works

### DoA Coordinate System

```
         0° (FRONT)
            ↑
            |
  270° ←----+----→ 90°
  (LEFT)    |    (RIGHT)
            |
            ↓
        180° (BACK)
```

### Example Output

```
🗣️ SPEAKING | DoA: 045° | FRONT-RIGHT    ↗ | Yaw: +15.0°
   → Turning head to +15.0°

🔇 Quiet    | DoA: 090° | RIGHT           → | Yaw: +30.0°

🗣️ SPEAKING | DoA: 270° | LEFT            ← | Yaw: -30.0°
   → Turning head to -30.0°
```

## Code Structure

```
doa_demo.py
├── Constants & Configuration
│   ├── DoA sampling interval
│   └── Head movement limits
│
├── Helper Functions
│   ├── angle_to_yaw()      # Convert DoA angle to robot head yaw
│   └── display_doa_info()  # Pretty console output
│
├── Main Loop
│   └── run_doa_demo()      # Continuous DoA monitoring & head tracking
│
└── Initialization
    └── init_robot()        # Connect to real robot
```

## Key Concepts

### 1. ReSpeaker Microphone Array
- 4 microphones arranged in a circle
- Calculates sound direction using time-delay between mics
- Built into Reachy Mini's head

### 2. DoA Data Structure
```python
doa_data = robot.media.audio.get_DoA()
# Returns: {'angle': 45, 'is_speaking': True}
```

- `angle`: Direction in degrees (0-360)
- `is_speaking`: Boolean, True when speech detected

### 3. Coordinate Conversion
- DoA gives absolute direction (0-360°)
- Robot head uses yaw (-30° to +30°)
- Code converts and clamps to robot limits

## Customization

### Adjust Sensitivity
```python
# In doa_demo.py, line 35
DOA_SAMPLE_INTERVAL = 0.1  # Faster = more responsive (but more CPU)
```

### Change Head Movement Range
```python
# In doa_demo.py, lines 38-39
MAX_YAW = 30.0   # Increase for wider turns (careful!)
MIN_YAW = -30.0
```

### Adjust Response Speed
```python
# In run_doa_demo(), line 165
duration=0.3  # Decrease for faster turns, increase for smoother
```

## Troubleshooting

**Error: `AttributeError: 'GstWebRTCClient' object has no attribute '_respeaker'`**
- ✅ This is EXPECTED on Mac!
- This error occurs because DoA requires direct hardware access
- Solution: Deploy app to robot - will work when running on robot itself

**Error: `libnice elements are not available`**
- ✅ This is the WebRTC issue on Mac (expected)
- Not fixable on Mac for remote connection
- Solution: Code needs to run on robot, not remotely from Mac

**When deployed to robot - troubleshooting:**

**Robot doesn't respond to sound:**
- Check that you're speaking loudly enough
- Make sure you're within 2-3 meters of robot
- Verify robot is connected (check movements work first)

**Head moves erratically:**
- Reduce ambient noise in the room
- Increase `DOA_SAMPLE_INTERVAL` for more stability
- Ensure only one person is speaking at a time

**Connection errors:**
- Make sure robot is powered on and on same WiFi
- Test with simple movement script first
- Check dashboard: http://reachy-mini.local:8000/

## Next Steps

**Enhancements you could add:**
- Combine with emotion expressions (turn + show curious emotion)
- Add voice response (turn + speak greeting)
- Track multiple speakers
- Create interactive games (follow the leader)
- Integrate with computer vision (turn to face + recognize person)

## Technical Notes

- Uses `media_backend="no_media"` to avoid WebRTC issues
- Only needs sensor data access, not audio streaming
- Head yaw limited to ±30° for safety
- Sampling at 10Hz (0.1s interval) balances responsiveness and CPU

---

**Related Projects:**
- `emoji_robot/` - Emotion expressions with audio/voice
- `choreography_demo/` - Pre-programmed dance routines

**See Also:**
- Main project README: `~/Documents/Workspace/reachy_mini_projects/README.md`
- SDK Documentation: https://github.com/pollen-robotics/reachy_mini
