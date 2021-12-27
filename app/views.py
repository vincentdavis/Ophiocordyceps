import random
import sys
import time
import pandas as pd
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import Power
import logging
log = logging.getLogger(__name__)
PowerModule = Power.Power()









class LandingView(TemplateView):
    template_name = "index.html"


class FileLoad(APIView):
    def post(self, request, format=None):
        try:
            log.info("Uploaded file :" +str(request.FILES['file']))
            df = pd.read_csv(request.FILES['file'])
            power = df.to_dict().get('power', None)
            cadence = df.to_dict().get('cadence', None)
            response = []
            if power and cadence:
                # forming list
                if len(power) == len(cadence):
                    for i, j in power.items():
                        response.append([power.get(i), cadence.get(i)])
            return Response(response)
        except Exception as e:
            log.error("Error in File Upload Api"+str(e))
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

            log.info("PW:{},PV:{},WPR1:{},WPR2:{},COR:{},PRL:{} ".format(
                str(PW),
                str(PV),
                str(WPR1),
                str(WPR2),
                str(COR),
                str(PRL)
            ))

            response = None
            antnode = None


            last = 0
            stopped = True
            power = None
            cadence = 0
            r = 1

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
                    power = PW_O if PW_O and PW_O != 'null' else power
                    cadence = COR_O if COR_O and  COR_O!='null'  else cadence

                    if power:
                        try:
                            PowerModule.power_meter.update(power, cadence)
                            log.info("Power Updated: {} , {}".format(str(power), str(cadence)))
                        except Exception as e:
                            log.error("Exception in power update: {}".format(str(e)))
                            pass
                        stopped = False
                    elif not stopped:
                        try:
                            PowerModule.power_meter.update(power, cadence)
                            log.info("Power Updated: {} , {}".format(str(power), str(cadence)))
                        except Exception as e:
                            log.error("Exception in power update: {}".format(str(e)))
                        stopped = True
                    last = t
                return Response({
                    "power": power,
                    "cadence": cadence,
                })
                # master.update_idletasks()
                # master.update()
            except (KeyboardInterrupt, SystemExit) as e:
                log.error("Exception: ", str(r))

        except Exception as e:
            log.error("Exception: " + repr(e))
            response = str(repr(e))
            if getattr(sys, 'frozen', False):
                input()
        finally:
            if not PowerModule.pywin32:
                PowerModule.stop_ant()
        return Response(response)


