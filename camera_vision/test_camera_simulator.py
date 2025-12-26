"""
Camera Test - Verify camera works with simulator using OpenCV backend.

This tests whether we can use the camera WITHOUT GStreamer by using
the "default" media backend which uses OpenCV for video capture.

Based on SDK research findings:
- Simulator streams camera via UDP on 127.0.0.1:5005
- OpenCV VideoCapture reads the UDP stream directly
- Working example exists in SDK: /utils/rerun.py
- Resolution: 1280x720 @ 60fps

Expected result: Camera window showing simulator view with FPS counter.
"""

from reachy_mini import ReachyMini
import cv2
import time

print("=" * 60)
print("CAMERA TEST - Simulator with OpenCV Backend")
print("=" * 60)

print("\n⚠️  Make sure simulator is running in another terminal!")
print("   (Run: reachy-sim)\n")
input("Press Enter when simulator is ready...")

print("\n🔌 Connecting to simulator with OpenCV camera...")
try:
    # Use DEFAULT backend - it uses OpenCV for camera!
    # The SDK automatically connects to udp://@127.0.0.1:5005 for simulator
    robot = ReachyMini(
        localhost_only=True,
        media_backend="default"  # OpenCV + SoundDevice (ignore audio warnings)
    )
    print("✅ Connected!")

    # Check if camera is available
    if robot.media is None or robot.media.camera is None:
        print("❌ Camera not available!")
        print("   Make sure simulator is running!")
        exit(1)

    print("✅ Camera interface ready!")
    print(f"   Backend: OpenCV VideoCapture")
    print(f"   Stream: UDP from simulator (127.0.0.1:5005)")
    print(f"   Resolution: {robot.media.camera._resolution}")

    print("\n📷 Capturing frames from simulator camera...")
    print("   Press 'q' to quit\n")

    frame_count = 0
    start_time = time.time()

    while True:
        # Get frame from camera using SDK method
        frame = robot.media.get_frame()

        if frame is not None:
            frame_count += 1

            # Calculate FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            # Add info overlay to frame
            cv2.putText(
                frame,
                "Reachy Mini Simulator - OpenCV Backend",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"FPS: {fps:.1f} | Frames: {frame_count}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"Resolution: {frame.shape[1]}x{frame.shape[0]}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                "Press 'q' to quit",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Display frame
            cv2.imshow("Reachy Mini Simulator Camera", frame)

            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n👋 Quitting...")
                break
        else:
            print("⚠️  No frame received (is simulator running?)")
            time.sleep(0.1)

    # Cleanup
    cv2.destroyAllWindows()

    print(f"\n📊 Statistics:")
    print(f"   Total frames: {frame_count}")
    print(f"   Average FPS: {fps:.1f}")
    print(f"   Duration: {elapsed:.1f}s")
    print("\n✅ Camera test successful!")
    print("   ✓ OpenCV backend works with simulator")
    print("   ✓ No GStreamer required")
    print("   ✓ Ready for computer vision projects!")

except KeyboardInterrupt:
    print("\n\n👋 Interrupted by user")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure simulator is running (reachy-sim)")
    print("2. Check that simulator started successfully")
    print("3. Verify camera stream on UDP port 5005")
    import traceback
    traceback.print_exc()

finally:
    print("\nDisconnecting...")
