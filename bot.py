#!/usr/bin/env python
import sys
import time
import platform
import random
import tkinter as tk

from ant.core import driver
from ant.core import node

from usb.core import find

from PowerMeterTx import PowerMeterTx
from config import DEBUG, LOG, NETKEY, POWER_SENSOR_ID

antnode = None
power_meter = None


def stop_ant():
    if power_meter:
        print("Closing power meter")
        power_meter.close()
        power_meter.unassign()
    if antnode:
        print("Stopping ANT node")
        antnode.stop()


pywin32 = False
if platform.system() == 'Windows':
    def on_exit(sig, func=None):
        stop_ant()


    try:
        import win32api

        win32api.SetConsoleCtrlHandler(on_exit, True)
        pywin32 = True
    except ImportError:
        print("Warning: pywin32 is not installed, use Ctrl+C to stop")


def disable_event():
    pass


try:
    # devs = find(find_all=True, idVendor=0x0fcf)
    # for dev in devs:
    #     if dev.idProduct in [0x1008, 0x1009]:
    #         stick = driver.USB2Driver(log=LOG, debug=DEBUG, idProduct=dev.idProduct, bus=dev.bus, address=dev.address)
    #         try:
    #             stick.open()
    #         except:
    #             continue
    #         stick.close()
    #         break
    # else:
    #     print("No ANT devices available")
    #     if getattr(sys, 'frozen', False):
    #         input()
    #     sys.exit()

    # antnode = node.Node(stick)
    # print("Starting ANT node")
    # antnode.start()
    # key = node.Network(NETKEY, 'N:ANT+')
    # antnode.setNetworkKey(0, key)

    print("Starting power meter with ANT+ ID " + repr(POWER_SENSOR_ID))
    try:
        # Create the power meter object and open it
        power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
        power_meter.open()
    except Exception as e:
        print("power_meter error: " + repr(e))
        power_meter = None

    # TODO Replace this with new gui.
    # TODO Add Gui options as requested below
    master = tk.Tk()
    master.title("Bot")
    master.geometry("200x50")
    master.resizable(False, False)
    master.call('wm', 'attributes', '.', '-topmost', '1')
    master.protocol("WM_DELETE_WINDOW", disable_event)
    w = tk.Scale(master, from_=10, to=1000, length=200, orient=tk.HORIZONTAL)
    w.pack()

    last = 0
    stopped = True
    power = None

    print("Main wait loop")
    while True:
        try:
            t = int(time.time())
            r = 1
            if t >= last + 1:
                if not power:
                    power = w.get()
                    print("power ->",power)
                    # TODO have a gui option for this random int range. Call it "Power Variability"
                    r = random.randint(-5, 5)
                    # TODO Would like to have optons for the .75 and 1.25 "Within power range"
                if (power * .75) < power + r < (power * 1.25):
                    power = power + r
                else:
                    power = power - r
                # TODO have a gui option for this random int range call it "Cadence offset range"
                cadence = 85 + random.randint(-5, 5)
                # TODO have a gui option for this random int range call it "Power range limits"
                power = w.get() + random.randint(0, 15)
                if power:
                    # power_meter.update(power, cadence)
                    print(power, cadence)
                    stopped = False
                elif not stopped:
                    # power_meter.update(power)
                    stopped = True
                last = t
            master.update_idletasks()
            master.update()
        except (KeyboardInterrupt, SystemExit):
            break

except Exception as e:
    print("Exception: " + repr(e))
    if getattr(sys, 'frozen', False):
        input()
finally:
    if not pywin32:
        stop_ant()