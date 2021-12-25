#!/usr/bin/env python
"""
Power module to send power
"""
import platform
from ant.core import driver
from ant.core import node
from usb.core import find
from PowerMeterTx import PowerMeterTx
from config import DEBUG, LOG, NETKEY, POWER_SENSOR_ID
import sys
import logging
log = logging.getLogger(__name__)

class Power(object):
    """
    Power Class
    """
    def platform_check(self):
        if platform.system() == 'Windows':
            def on_exit(sig, func=None):
                self.stop_ant()

            try:
                import win32api

                win32api.SetConsoleCtrlHandler(on_exit, True)
                self.pywin32 = True
            except ImportError:
                log.info("Warning: pywin32 is not installed, use Ctrl+C to stop")

    def stop_ant(self):
        if self.power_meter:
            log.info("Closing power meter")
            self.power_meter.close()
            self.power_meter.unassign()
        if self.antnode:
            log.info("Stopping ANT node")
            self.antnode.stop()

    def getstick(self):
        try:
            devs = find(find_all=True, idVendor=0x0fcf)
            for dev in devs:
                if dev.idProduct in [0x1008, 0x1009]:
                    self.stick = driver.USB2Driver(log=LOG, debug=DEBUG, idProduct=dev.idProduct, bus=dev.bus,
                                              address=dev.address)
                    try:
                        self.stick.open()
                    except:
                        continue
                    self.stick.close()
                    break
            else:
                log.info("No ANT devices available")
                if getattr(sys, 'frozen', False):
                    input()
            self.antnode = node.Node(self.stick)
            log.info("Starting ANT node")
            self.antnode.start()
            key = node.Network(NETKEY, 'N:ANT+')
            self.antnode.setNetworkKey(0, key)
        except Exception as e:
            log.error("Error: Exception in connecting device:"+str(e) )
            pass

    def createPowerMeterObj(self):
        try:
            # Create the power meter object and open it
            self.power_meter = PowerMeterTx(self.antnode, POWER_SENSOR_ID)
            self.power_meter.open()
        except Exception as e:
            log.error("power_meter error: "+str(repr(e)))
            self.power_meter = None

    def __init__(self) -> None:
        self.power_meter = None
        self.antnode = None
        self.pywin32 = False
        self.stick = None
        self.platform_check()
        self.getstick()
        log.info("Starting power meter with ANT+ ID " + repr(POWER_SENSOR_ID))
        self.createPowerMeterObj()
        super().__init__()