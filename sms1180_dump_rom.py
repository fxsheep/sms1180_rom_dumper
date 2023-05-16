#!/usr/bin/env python3
import sys,usb
from sms1180usb import *

MSG_SMS_RD_MEM_REQ    = 552

dev = usb.core.find(idVendor=0x187f, idProduct=0x0300)
if (dev == None):
    print("No SMS1180 device found")
    exit()
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)
dev.set_configuration()

sms1180 = SMS1180USB(dev)

dump = open("sms1180_rom_dump_0x0.bin", mode='wb')

for addr in range(0, 0x20000, 4):
    sms1180.msg_send_req(MSG_SMS_RD_MEM_REQ, struct.pack("<II", addr, 4))
    ret = sms1180.msg_get_resp()
    if len(ret) == 1:
        continue
    else:
        dump.write(ret[1])

