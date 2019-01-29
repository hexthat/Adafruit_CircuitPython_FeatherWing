# The MIT License (MIT)
#
# Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_featherwing.alphanum_featherwing`
====================================================

Helper for using the `14-Segment AlphaNumeric FeatherWing <https://www.adafruit.com/product/3139>`_.

* Author(s): Melissa LeBlanc-Williams
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FeatherWing.git"

from time import sleep
import adafruit_ht16k33.segments as segments
from adafruit_featherwing import shared

class AlphaNumFeatherWing:
    """Class representing an `Adafruit 14-segment AlphaNumeric FeatherWing
       <https://www.adafruit.com/product/3139>`_.

       Automatically uses the feather's I2C bus."""
    def __init__(self, address=0x70):
        self._seg14x4 = segments.Seg14x4(shared.I2C_BUS, address)
        self._seg14x4.auto_write = False

    def print(self, value):
        """
        Print a number or text to the display

        :param value: The text to display
        :type value: str, int or float

        .. code-block:: python
            from adafruit_featherwing import alphanum_featherwing

            display = alphanum_featherwing.AlphaNumFeatherWing()
            display.print(1234)
        """
        self._seg14x4.print(value)
        self._seg14x4.show()

    def marquee(self, text, delay=0.25, loop=True):
        """
        Automatically scroll the text at the specified delay between characters

        :param str text: The text to display
        :param float delay: (optional) The delay in seconds to pause before scrolling
                            to the next character (default=0.25)
        :param bool loop: (optional) Whether to endlessly loop the text (default=True)

        .. code-block:: python

            from adafruit_featherwing import alphanum_featherwing

            display = alphanum_featherwing.AlphaNumFeatherWing()
            display.marquee('This is some really long text  ')
        """
        if isinstance(text, str):
            self.fill(False)
            if loop:
                while True:
                    self._scroll_marquee(text, delay)
            else:
                self._scroll_marquee(text, delay)

    def _scroll_marquee(self, text, delay):
        for character in text:
            self._seg14x4.scroll()
            self._seg14x4[3] = character
            sleep(delay)
            self._seg14x4.show()

    @property
    def blink_rate(self):
        """Blink Rate returns the current rate that the text blinks.
        0 = Off
        1-3 = Successively slower blink rates

        This example changes the blink rate and prints out the current setting

        .. code-block:: python

            from adafruit_featherwing import alphanum_featherwing
            from time import sleep

            display = alphanum_featherwing.AlphaNumFeatherWing()
            display.print('Text')

            for blink_rate in range(3, -1, -1):
                display.blink_rate = blink_rate
                print("Current Blink Rate is {}".format(display.blink_rate))
                sleep(4)
        """
        return self._seg14x4.blink_rate

    @blink_rate.setter
    def blink_rate(self, rate):
        self._seg14x4.blink_rate = rate

    @property
    def brightness(self):
        """Brightness returns the current display brightness.
        0-15 = Dimmest to Brightest Setting

        This example changes the brightness and prints out the current setting

        .. code-block:: python

            from adafruit_featherwing import alphanum_featherwing
            from time import sleep

            display = alphanum_featherwing.AlphaNumFeatherWing()
            display.print('Text')

            for brightness in range(0, 16):
                display.brightness = brightness
                print("Current Brightness is {}".format(display.brightness))
                sleep(0.2)
        """
        return self._seg14x4.brightness

    @brightness.setter
    def brightness(self, brightness):
        self._seg14x4.brightness = brightness

    def fill(self, fill):
        """Change all Segments on or off
        :param bool fill: True turns all segments on, False turns all segments off

        This example alternates between all filled and all empty segments.

        .. code-block:: python

            from adafruit_featherwing import alphanum_featherwing
            from time import sleep

            display = alphanum_featherwing.AlphaNumFeatherWing()

            while True:
                display.fill(True)
                sleep(0.5)
                display.fill(False)
                sleep(0.5)
        """
        if isinstance(fill, bool):
            self._seg14x4.fill(1 if fill else 0)
            self._seg14x4.show()
        else:
            raise ValueError('Must set to either True or False.')
