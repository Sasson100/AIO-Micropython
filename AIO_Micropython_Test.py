# this test uses the ESP32 led for the led_callback function, change the pin that is switched in it to change it to your microprocessor
from AIO_Micropython import AIO_MP
from machine import Pin
wifi_ssid='*wifi name*'
wifi_password='*wifi password*'
aio_username='*aio username*'
aio_key='*aio key*'
client_id='*client id, name it whatever you want*' # this is optional
aio=AIO_MP(wifi_ssid,wifi_password,aio_username,aio_key,client_id)


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
