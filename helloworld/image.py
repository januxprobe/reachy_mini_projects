import cv2
from reachy_mini import ReachyMini

try:
    with ReachyMini(localhost_only=False) as mini:
        frame = mini.media.get_frame()
        if frame is not None and frame.size > 0:
            cv2.imshow("Reachy", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: Could not retrieve frame from camera.")
except ModuleNotFoundError as e:
    if 'gst_signalling' in str(e):
        print("Error: Missing required module 'gst_signalling'.")
        print("\nTo install gst-signalling, you first need to install system dependencies:")
        print("  brew install pkg-config cairo gobject-introspection gstreamer gst-plugins-base")
        print("\nThen install the Python package:")
        print("  pip install gst-signalling")
        print("\nAlternatively, if you don't need camera access, use:")
        print("  ReachyMini(localhost_only=False, media_backend='no_media')")
    else:
        raise
except KeyError as e:
    error_msg = str(e)
    if 'Producer' in error_msg and 'not found' in error_msg:
        print("Error: Media producer not found on the robot.")
        print("\nTo enable the media backend on your Reachy Mini:")
        print("\n1. Check the Robot Dashboard:")
        print("   - Open http://ROBOT_IP:8000 in your browser")
        print("   - Look for camera/media settings or status")
        print("   - Ensure the camera is enabled in the dashboard")
        print("\n2. Restart the Robot:")
        print("   - Power cycle the robot (turn off and on)")
        print("   - The media service should start automatically on boot")
        print("\n3. Verify Camera Hardware:")
        print("   - Ensure the camera is properly connected to the robot")
        print("   - Check if the camera appears in the robot's hardware list")
        print("\n4. Check Media Service Status (if you have SSH access):")
        print("   - SSH into the robot: ssh reachy@ROBOT_IP")
        print("   - Check if media services are running")
        print("   - Restart services if needed: sudo systemctl restart reachy-media")
        print("\n5. Alternative - Use no_media backend:")
        print("   If you don't need camera access, use:")
        print("   ReachyMini(localhost_only=False, media_backend='no_media')")
    else:
        raise
except Exception as e:
    error_msg = str(e)
    if 'pkg-config' in error_msg or 'cairo' in error_msg or 'PyGObject' in error_msg:
        print("Error: Missing system dependencies required for gst-signalling.")
        print("\nOn macOS, install the required dependencies with Homebrew:")
        print("  brew install pkg-config cairo gobject-introspection gstreamer gst-plugins-base")
        print("\nThen try installing gst-signalling again:")
        print("  pip install gst-signalling")
        print("\nAlternatively, if you don't need camera access, use:")
        print("  ReachyMini(localhost_only=False, media_backend='no_media')")
    else:
        print(f"Error: {error_msg}")
        raise