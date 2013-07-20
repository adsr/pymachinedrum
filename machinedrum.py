#!/usr/bin/python
#
# Module for generating Elektron Machinedrum MIDI messages
# Each method returns a list of integers representing a MIDI message
#
# Adam Saponara
# adam TA atoi TOD cc
#
# Changelog:
#
#    20-Jul-2013: initial release

class Machinedrum():
    def __init__(self):
        self.sysex_header = [0xf0, 0x00, 0x20, 0x3c, 0x02, 0x00]
        self.sysex_footer = [0xf7]
    def trig(self, track, vel):
        note = [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62][val16(track)]
        return [0x90, note, val128(vel)]
    def set_track_param(self, track, param, val):
        track = val16(track)
        chan = track / 4
        offset = track % 4
        return [0xb0 + chan, [16, 40, 72, 96][offset] + val24(param), val128(val)]
    def set_track_level(self, track, level):
        track = val16(track)
        chan = track / 4
        offset = track % 4
        return [0xb0 + chan, [8, 9, 10, 11][offset], val128(level)]
    def set_track_mute(self, track, mute):
        track = val16(track)
        chan = track / 4
        offset = track % 4
        return [0xb0 + chan, [12, 13, 14, 15][offset], val128(mute)]
    def set_delay_param(self, param, val):
        return self.__get_sysex([0x5d, val8(param), val128(val)])
    def set_reverb_param(self, param, val):
        return self.__get_sysex([0x5e, val8(param), val128(val)])
    def set_eq_param(self, param, val):
        return self.__get_sysex([0x5f, val8(param), val128(val)])
    def set_compressor_param(self, param, val):
        return self.__get_sysex([0x60, val8(param), val128(val)])
    def set_tempo(self, bpm):
        bpm = int(min(max(float(bpm), 30.0), 300.0) * 24.0)
        return self.__get_sysex([0x61, (bpm >> 7) & 0x7f, bpm & 0x7f])
    def set_lfo_param(self, lfo, param, val):
        lfo = val16(lfo)
        param = val8(param)
        val = val128(val)
        return self.__get_sysex([0x62, (lfo << 3) | param, val])
    def mute_track(self, track):
        return self.set_track_mute(track, 1)
    def unmute_track(self, track):
        return self.set_track_mute(track, 0)
    def __get_sysex(self, list):
        vals = []
        vals.extend(self.sysex_header)
        vals.extend(list)
        vals.extend(self.sysex_footer)
        return vals

def fval(mod):
    return lambda val: abs(int(val) % mod)

val8 = fval(8)
val16 = fval(16)
val24 = fval(24)
val128 = fval(128)

if __name__ == "__main__":
    import sys
    import os
    md = Machinedrum()
    if len(sys.argv) > 1 and hasattr(md, sys.argv[1]):
        print getattr(md, sys.argv[1])(*sys.argv[2:])
    else:
        print "Usage: ./%s <method> [arg1 [arg2 ...]]" % os.path.basename(__file__)
