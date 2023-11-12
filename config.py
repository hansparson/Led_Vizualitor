"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import sys, os
frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        basis = sys.argv[0]
        required_folder = os.path.split(basis)[0]

print( 'we are',frozen,'frozen')
print( 'bundle dir is', bundle_dir )
print( 'sys.argv[0] is', sys.argv[0] )
print( 'sys.executable is', sys.executable )
print( 'os.getcwd is', os.getcwd() )

root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('Tambahkan Device Baru')

# store email address and password
email = tk.StringVar()
password = tk.StringVar()


def login_clicked():
    """ callback when the login button clicked
    """
    msg = f'IP Device LED: {email.get()} Jumlah LED : {password.get()}'
    showinfo(
        title='Information',
        message=msg
    )
    root.quit()
    root.destroy()


# Sign in frame
signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)
# email
email_label = ttk.Label(signin, text="IP Device LED:")
email_label.pack(fill='x', expand=True)
email_entry = ttk.Entry(signin, textvariable=email)
email_entry.pack(fill='x', expand=True)
email_entry.focus()
# password
password_label = ttk.Label(signin, text="Jumlah LED :")
password_label.pack(fill='x', expand=True)
password_entry = ttk.Entry(signin, textvariable=password)
password_entry.pack(fill='x', expand=True)
# login button
login_button = ttk.Button(signin, text="Daftarkan Device Apex LED", command=login_clicked)
login_button.pack(fill='x', expand=True, pady=10)
root.mainloop()

DEVICE = 'esp8266'
#DEVICE = 'pi'
"""Device used to control LED strip. Must be 'pi',  'esp8266' or 'blinkstick'

'esp8266' means that you are using an ESP8266 module to control the LED strip
and commands will be sent to the ESP8266 over WiFi.

'pi' means that you are using a Raspberry Pi as a standalone unit to process
audio input and control the LED strip directly.

'blinkstick' means that a BlinkstickPro is connected to this PC which will be used
to control the leds connected to it.
"""

if DEVICE == 'esp8266':
    UDP_IP = '{}'.format(email.get())
    """IP address of the ESP8266. Must match IP in ws2812_controller.ino"""
    UDP_PORT = 7777
    """Port number used for socket communication between Python and ESP8266"""
    SOFTWARE_GAMMA_CORRECTION = False
    """Set to False because the firmware handles gamma correction + dither"""

if DEVICE == 'pi':
    LED_PIN = 18
    """GPIO pin connected to the LED strip pixels (must support PWM)"""
    LED_FREQ_HZ = 800000
    """LED signal frequency in Hz (usually 800kHz)"""
    LED_DMA = 5
    """DMA channel used for generating PWM signal (try 5)"""
    BRIGHTNESS = 255
    """Brightness of LED strip between 0 and 255"""
    LED_INVERT = True
    """Set True if using an inverting logic level converter"""
    SOFTWARE_GAMMA_CORRECTION = True
    """Set to True because Raspberry Pi doesn't use hardware dithering"""

if DEVICE == 'blinkstick':
    SOFTWARE_GAMMA_CORRECTION = True
    """Set to True because blinkstick doesn't use hardware dithering"""

USE_GUI = True
"""Whether or not to display a PyQtGraph GUI plot of visualization"""

DISPLAY_FPS = True
"""Whether to display the FPS when running (can reduce performance)"""

N_PIXELS = int(password.get())
"""Number of pixels in the LED strip (must match ESP8266 firmware)"""

GAMMA_TABLE_PATH = os.path.join(os.getcwd(), 'gamma_table.npy')
"""Location of the gamma correction table"""

MIC_RATE = 44100
"""Sampling frequency of the microphone in Hz"""

FPS = 60
"""Desired refresh rate of the visualization (frames per second)

FPS indicates the desired refresh rate, or frames-per-second, of the audio
visualization. The actual refresh rate may be lower if the computer cannot keep
up with desired FPS value.

Higher framerates improve "responsiveness" and reduce the latency of the
visualization but are more computationally expensive.

Low framerates are less computationally expensive, but the visualization may
appear "sluggish" or out of sync with the audio being played if it is too low.

The FPS should not exceed the maximum refresh rate of the LED strip, which
depends on how long the LED strip is.
"""
_max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = 200
"""Frequencies below this value will be removed during audio processing"""

MAX_FREQUENCY = 12000
"""Frequencies above this value will be removed during audio processing"""

N_FFT_BINS = 24
"""Number of frequency bins to use when transforming audio to frequency domain

Fast Fourier transforms are used to transform time-domain audio data to the
frequency domain. The frequencies present in the audio signal are assigned
to their respective frequency bins. This value indicates the number of
frequency bins to use.

A small number of bins reduces the frequency resolution of the visualization
but improves amplitude resolution. The opposite is true when using a large
number of bins. More bins is not always better!

There is no point using more bins than there are pixels on the LED strip.
"""

N_ROLLING_HISTORY = 2
"""Number of past audio frames to include in the rolling window"""

MIN_VOLUME_THRESHOLD = 1e-7
"""No music visualization displayed if recorded audio volume below threshold"""
