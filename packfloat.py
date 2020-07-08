# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Lee Nelson for nelnet.org
#
# SPDX-License-Identifier: MIT
"""
`packfloat`
================================================================================

CircuitPython utility class to turn a float into 2 8-byte integers suitable for transmission over a serial protocol


* Author(s): Lee Nelson

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/nelnet-teams/CircuitPython_packfloat.git"


class packFloat:
    def __init__(self, exponent=0):
        if exponent < 0 or exponenet > 7:
            raise Exception('Exponent must be in range 0-7: {} illegal'.format(exponent))
        self.exponent = exponent
        self.tenpower = 10 ** exponent
        self.flagmask = 0b10000000       # bit 7 of 0-7
        self.exponentmask = 0b01110000   # bits 4-6 of 0-7
        self.maxval = 0b111111111111     # 12 bits

    def pack_float(self, val):
        newval = val
        if self.tenpower > 0:
            newval = int(floatval * self.tenpower)
        if newval < 0:
            flag = 1
        else:
            flag=0
        newval = abs(newval)
        if newval > self.maxval:
            raise Exception('{} too large'.format(abs(val)))
        lsb = newval % 256
        newval = newval >> 8
        msb = newval % 16
        msb += (self.exponent << 4)
        msb += (self.flag << 7)
        return msb, lsb

    def unpack_float(self, msb, lsb):
        flag = msb & self.flagmask
        exponent = msb & self.exponentmask
        msb = msb % 16
        newval = lsb + (msb << 8)
        if flag:
            newval = newval * -1
        if self.tenpower > 0:
            newval = newval / self.tenpower
        return newval
