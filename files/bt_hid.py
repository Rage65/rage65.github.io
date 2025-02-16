#!/usr/bin/env python3

import evdev
import dbus
import time

def main():
    # 1. Get the Bluetooth adapter (if you’re doing Bluetooth stuff)
    bus = dbus.SystemBus()
    adapter = dbus.Interface(
        bus.get_object("org.bluez", "/org/bluez/hci0"),
        "org.freedesktop.DBus.Properties"
    )
    adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    # 2. Find keyboard and mouse devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    keyboard = None
    mouse = None

    for device in devices:
        # Adjust matching logic as needed for your device names
        if "keyboard" in device.name.lower():
            keyboard = device
        elif "mouse" in device.name.lower():
            mouse = device

    if not keyboard or not mouse:
        print("Keyboard or mouse not detected!")
        return

    print(f"Keyboard: {keyboard.name} ({keyboard.path})")
    print(f"Mouse: {mouse.name} ({mouse.path})")

    # 3. Define a helper function to read events in a loop
    def read_events(dev):
        # Grab the device for exclusive access
        dev.grab()
        print(f"Grabbed device: {dev.name}")
        try:
            for event in dev.read_loop():
                if event.type in [evdev.ecodes.EV_KEY, evdev.ecodes.EV_REL, evdev.ecodes.EV_ABS]:
                    print(f"Sending event from {dev.name}: {event}")
                    # Here is where you’d send the event over Bluetooth as HID
        except OSError:
            # This can happen if the device is disconnected or ungrabbed
            print(f"Lost device: {dev.name}")
        finally:
            # Always ungrab the device before exiting
            dev.ungrab()
            print(f"Ungrabbing device: {dev.name}")

    # 4. Read both devices in parallel (optional, you can do sequentially if you prefer)
    #    We’ll use threads so both keyboard and mouse events are captured at the same time.
    from threading import Thread
    k_thread = Thread(target=read_events, args=(keyboard,), daemon=True)
    m_thread = Thread(target=read_events, args=(mouse,), daemon=True)

    k_thread.start()
    m_thread.start()

    print("Press Ctrl+C to stop...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping script...")

if __name__ == "__main__":
    main()
