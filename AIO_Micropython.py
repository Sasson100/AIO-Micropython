import network
import time
from umqtt.simple import MQTTClient
import _thread

class AIO_MP:
    def __init__(self,ssid,password,aio_username,aio_key,client_id="ESP32"):
        # Wifi credentials
        self.ssid=ssid
        self.password=password
        # Adafruit IO credentials
        self.aio_username=aio_username
        self.aio_key=aio_key
        # MQTT client settings
        self.BROKER="io.adafruit.com"
        self.CLIENT_ID=client_id
        self.callbacks={}
        self.throttle=0
    
    def connect_to_internet(self):
        # Connecting to wifi
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        print("Connecting to WiFi...", end="")
        while not self.wlan.isconnected():
            time.sleep(1)
            print(".", end="")
        print("\nConnected to WiFi!")
        print("IP Address:", self.wlan.ifconfig()[0])
        # Connect to Adafruit IO
        self.client = MQTTClient(self.CLIENT_ID,self.BROKER, user=self.aio_username, password=self.aio_key)
        def def_callback(topic,msg):
            feed_name=topic.decode('utf-8').split("/")[-1]
            message=msg.decode('utf-8')
            if feed_name is "throttle":
                l=message.replace(f'{self.aio_username} ','')
                for char in l:
                    if not char.isdigit():
                        l=l.replace(char,'')
                print(f'You have reached the data rate limit, going to sleep for {l} seconds')
                self.throttle=1
                time.sleep(int(l)+1)
                print("Throttle has stopped")
                self.throttle=0
            elif feed_name is "error":
                print("There was an error:")
                print(message)
            else:
                print(f'Received message on the feed {feed_name}: {message}')
                if feed_name in self.callbacks:
                    self.callbacks[feed_name](message)
                else:
                    print(f'No callback registered for feed "{feed_name}"')
        self.client.set_callback(def_callback)  # Set the callback for received messages
        self.client.connect()
        print("Connected to Adafruit IO!")
        self.client.subscribe(f"{self.aio_username}/throttle")
        
    
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
                if self.throttle==0:
                    try:
                        self.client.check_msg()
                        time.sleep(0.1)
                    except Exception as e:
                        print(f'Reading feeds failed with the error:')
                        print(f'{type(e).__name__}: {e}')
                        time.sleep(5)
        _thread.start_new_thread(check_messages,())
