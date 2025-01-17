import network
import time
from umqtt.simple import MQTTClient
import _thread

class AIO_ESP:
    def __init__(self,ssid,password,aio_username,aio_key):
        # Wifi credentials
        self.ssid=ssid
        self.password=password
        # Adafruit IO credentials
        self.aio_username=aio_username
        self.aio_key=aio_key
        # MQTT client settings
        self.BROKER = "io.adafruit.com"
        self.CLIENT_ID = "ESP32"
        self.callbacks={}
    
    def connect_to_internet(self):
        # Connecting to wifi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        print("Connecting to WiFi...", end="")
        while not wlan.isconnected():
            time.sleep(1)
            print(".", end="")
        print("\nConnected to WiFi!")
        print("IP Address:", wlan.ifconfig()[0])
        # Connect to Adafruit IO
        self.client = MQTTClient(self.CLIENT_ID,self.BROKER, user=self.aio_username, password=self.aio_key,keepalive=60)
        def def_callback(topic,msg):
            feed_name=topic.decode('utf-8').split("/")[-1]
            print(f'Received message on the feed {feed_name}: {msg.decode("utf-8")}')
            if feed_name in self.callbacks:
                self.callbacks[feed_name](msg.decode('utf-8'))
            else:
                print(f'No callback registered for feed "{feed_name}"')
        self.client.set_callback(def_callback)  # Set the callback for received messages
        self.client.connect()
        print("Connected to Adafruit IO!")
    
    def subscribe_feed(self,feed_name):
        if self.client:
            self.client.subscribe(f"{self.aio_username}/feeds/{feed_name}")
            print(f'Subscribed to {feed_name}')
        else:
            print("Erro: Not connected to Adafruit IO")

    def register_callback(self,feed_name:str,callback):
        self.callbacks[feed_name]=callback
        print(f'Callback function {callback.__name__} registered to feed {feed_name}')

    def write_feed(self,feed_name,msg):
        if self.client:
            self.client.publish(f'{self.aio_username}/feeds/{feed_name}',str(msg))
        else:
            print("Error: Not connected to Adafruit IO")
    
    def read_feed(self):
        def check_messages():
            while True:
                self.client.check_msg()
        _thread.start_new_thread(check_messages,())
        _thread.start_new_thread(check_messages,())
