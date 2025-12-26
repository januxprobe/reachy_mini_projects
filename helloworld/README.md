# Reachy Mini - Hello World Project

Your first Reachy Mini robot application!

## What This Does

This simple program connects to your Reachy Mini robot and makes its antennas wiggle back and forth. It's the perfect first project to verify everything is working.

## How to Run (Wireless Robot)

### Step 1: Power On Your Robot
Turn on your Reachy Mini Wireless robot. The daemon starts automatically.

### Step 2: Connect to the Same Network
Make sure your MacBook and the robot are connected to the same WiFi network.

### Step 3: Find Your Robot's IP Address
You need to know your robot's IP address. Check:
- The robot's display/interface, or
- Your router's connected devices list, or
- Use `arp -a` or a network scanner

**Verify connection:** Open `http://ROBOT_IP:8000` in your browser (replace ROBOT_IP with the actual IP address). You should see the Reachy Dashboard.

### Step 4: Run Your Hello World App
Open a terminal window.

```bash
# Navigate to your project
cd ~/Documents/Workspace/reachy_mini_projects/helloworld

# Activate the environment using the quick alias
reachy

# Run your program
python hello.py
```

If you see the antennas move and the success message, congratulations! 🎉

## Quick Reference

**Activate environment from anywhere:**
```bash
reachy
```

**Your project location:**
```
~/Documents/Workspace/reachy_mini_projects/helloworld/
```

## Next Steps

- Modify `hello.py` to try different antenna positions
- Check out other examples in the [Reachy Mini GitHub repo](https://github.com/pollen-robotics/reachy_mini/tree/develop/examples)
- Read the [Python SDK documentation](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/python-sdk.md)
- Create new projects in `~/Documents/Workspace/reachy_mini_projects/`

## Troubleshooting

**"Command 'reachy' not found":**
Open a new terminal window or run: `source ~/.zshrc`

**"Cannot connect to Reachy Mini":**
- Make sure the robot is powered on
- Verify both devices are on the same WiFi network
- Check that you can access the dashboard at http://ROBOT_IP:8000
- Confirm the robot's IP address hasn't changed

**Need more help?**
Check the [Troubleshooting Guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/troubleshooting.md)
