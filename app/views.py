import platform
import random
import sys
import time
import pandas as pd
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


class FileLoad(APIView):
    def post(self, request, format=None):
        try:
            print(type(request.FILES['file']))
            df = pd.read_csv(request.FILES['file'])
            power = df.to_dict().get('power', None)
            cadence = df.to_dict().get('cadence', None)
            response = []
            if power and cadence:
                # forming list
                if len(power) == len(cadence):
                    for i, j in power.items():
                        response.append([power.get(i), cadence.get(i)])
            print(df.to_json())
            return Response(response)
        except Exception as e:
            print(str(e))
            return Response(False)




class Request(APIView):
    def get(self, request, format=None):
        try:
            PW = int(request.GET.get('PW'))
            PW_O = request.GET.get('PW_O', None)
            PV = int(request.GET.get('PV', None))
            WPR1 = float(request.GET.get('WPR1', None))
            WPR2 = float(request.GET.get('WPR2', None))
            COR = int(request.GET.get('COR', None))
            COR_O = request.GET.get('COR_O', None)
            PRL = int(request.GET.get('PRL', None))

            print("PW", PW)
            print("PV", PV)
            print("WPR1", WPR1)
            print("WPR2", WPR2)
            print("COR",COR)
            print("PRL", PRL)
            response = None
            antnode = None
            try:
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
            except Exception as e:
                pass
            print("Starting power meter with ANT+ ID " + repr(POWER_SENSOR_ID))
            try:
                # Create the power meter object and open it
                power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
                power_meter.open()
            except Exception as e:
                print("power_meter error: " + repr(e))
                power_meter = None

            last = 0
            stopped = True
            power = None
            cadence = 0
            r = 1

            print("Main wait loop")
            try:
                t = int(time.time())
                r = 1
                if t >= last + 1:
                    if not power:
                        power = PW
                        if PV:
                            r = PV
                        else:
                            r = random.randint(-5, 5)
                    if (power * WPR1) < power + r < (power * WPR1):
                        power = power + r
                    else:
                        power = power - r
                    if COR:
                        cadence = COR
                    else:
                        cadence = 85 + random.randint(-5, 5)
                    if PRL:
                        power = PW + PRL
                    else:
                        power = PW + random.randint(0, 15)
                    if power:
                        try:power_meter.update(PW_O if PW_O  else power, COR_O if COR_O else cadence)
                        except: pass
                        print(power, cadence)
                        stopped = False
                    elif not stopped:
                        try:power_meter.update(PW_O if PW_O  else power)
                        except : pass

                        stopped = True
                    last = t
                return Response({
                    "power": power,
                    "cadence": cadence,
                })
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


