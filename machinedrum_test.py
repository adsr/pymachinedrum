#!/usr/bin/python

import sys
import os
import pypm
from machinedrum import Machinedrum
try:
    import pyreadline
except ImportError:
    import readline

pypm.Initialize()

if len(sys.argv) < 2:
    print "Usage: ./%s <out_device_num>\n\nDevices:" % os.path.basename(__file__)
    print ("device_num", "iface", "name", "inputs", "outputs", "opened?",)
    for dev in range(pypm.CountDevices()):
        print dev, pypm.GetDeviceInfo(dev)
else:
    mout = pypm.Output(int(sys.argv[1]), 0)
    md = Machinedrum()
    while True:
        input = raw_input(">")
        if len(input) < 1:
            break
        args = [arg.strip() for arg in input.split(' ')]
        if hasattr(md, args[0]):
            msg = getattr(md, args[0])(*args[1:])
            print msg
            if len(msg) == 3:
                mout.WriteShort(*msg)
            else:
                mout.WriteSysEx(0, msg)

del mout
pypm.Terminate()
