import evdev
import dbus
import time

# Get Bluetooth device
bus = dbus.SystemBus()
adapter = dbus.Interface(bus.get_object("org.bluez", "/org/bluez/hci0"), "org.freedesktop.DBus.Properties")
adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

# Find keyboard and mouse devices
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
keyboard = None
mouse = None

for device in devices:
    if "keyboard" in device.name.lower():
        keyboard = device
    elif "mouse" in device.name.lower():
        mouse = device

if not keyboard or not mouse:
    print("Keyboard or mouse not detected!")
    exit(1)

print("Keyboard:", keyboard.name)
print("Mouse:", mouse.name)

# Loop to read and send events
def send_events(device):
    for event in device.read_loop():
        if event.type in [evdev.ecodes.EV_KEY, evdev.ecodes.EV_REL, evdev.ecodes.EV_ABS]:
            # Here, send input events over Bluetooth
            print(f"Sending event: {event}")

# Run the input event loop
try:
    send_events(keyboard)
    send_events(mouse)
except KeyboardInterrupt:
    print("Stopping...")
