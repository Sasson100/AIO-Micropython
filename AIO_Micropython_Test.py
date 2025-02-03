from AIO_Micropython import AIO_MP
from machine import Pin
wifi_ssid='*wifi name*'
wifi_password='*wifi password'
aio_username='*aio username*'
aio_key='*aio key*'
aio=AIO_MP(wifi_ssid,wifi_password,aio_username,aio_key)


aio.connect_to_internet()
def led_callback(msg):
    if msg is "ON":
        Pin(2,Pin.OUT).value(1)
    else:
        Pin(2,Pin.OUT).value(0)
# I made this test when I was still making the library, so the temperature feed was just connected to a slider
def temperature_callback(msg):
    temperature = float(msg)
    if temperature<=20:
        aio.write_feed("temperaturemessage",f"Today it'll be {temperature} degrees, put a jacket on")
    else:
        aio.write_feed("temperaturemessage",f"Today it'll be {temperature} degrees, it'll be a nice day today")

aio.register_callback("ledSwitch",led_callback)
aio.register_callback("temperature",temperature_callback)
aio.subscribe_feed("ledSwitch")
aio.subscribe_feed("temperature")

aio.read_feed()
