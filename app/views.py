import platform
import random
import sys
import time

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

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




class LandingView(TemplateView):
    template_name = "index.html"


class Request(APIView):
    def get(self, request, format=None):
        try:
            print("PW", request.GET.get('PW'))
            print("PW", request.GET.get('PV'))
            print("WPR1", request.GET.get('WPR1'))
            print("WPR2", request.GET.get('WPR2'))
            print("COR",request.GET.get('COR'))
            print("PRL", request.GET.get('PRL'))
            response = None
            devs = find(find_all=True, idVendor=0x0fcf)
            for dev in devs:
                if dev.idProduct in [0x1008, 0x1009]:
                    stick = driver.USB2Driver(log=LOG, debug=DEBUG, idProduct=dev.idProduct, bus=dev.bus,
                                              address=dev.address)
                    try:
                        stick.open()
                    except:
                        continue
                    stick.close()
                    break
            else:
                print("No ANT devices available")
                if getattr(sys, 'frozen', False):
                    input()
                sys.exit()

            antnode = node.Node(stick)
            print("Starting ANT node")
            antnode.start()
            key = node.Network(NETKEY, 'N:ANT+')
            antnode.setNetworkKey(0, key)

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
            last = 0
            stopped = True
            power = None
            r = 1

            print("Main wait loop")
            try:
                t = int(time.time())
                if t >= last + 1:
                    if not power:
                        power = request.GET.get('PW')
                        # TODO have a gui option for this random int range. Call it "Power Variability"
                        r = request.GET.get('PV')
                        # TODO Would like to have optons for the .75 and 1.25 "Within power range"
                    if (power * request.GET.get('WPR1')) < power + r < (power * request.GET.get('WPR2')):
                        power = power + r
                    else:
                        power = power - r
                    # TODO have a gui option for this random int range call it "Cadence offset range"
                    cadence = request.GET.get('COR')
                    # TODO have a gui option for this random int range call it "Power range limits"
                    power = request.GET.get('power') + request.GET.get('PRL')
                    if power:
                        power_meter.update(power, cadence)
                        stopped = False
                    elif not stopped:
                        power_meter.update(power)
                        stopped = True
                    last = t
                # master.update_idletasks()
                # master.update()
            except (KeyboardInterrupt, SystemExit):
                pass

        except Exception as e:
            print("Exception: " + repr(e))
            response = str(repr(e))
            if getattr(sys, 'frozen', False):
                input()
        finally:
            if not pywin32:
                stop_ant()
        return Response(response)


