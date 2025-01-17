# AIO-ESP32-Micropython
This library is a class that lets an esp32 communicate with Adafruit IO through Micropython, it might work with other microprocessors that use Micropython and have wifi, but I haven't tested that

**This library is dependant on the `umqtt.simple` library**

# How to use (Look at the AIO_ESP32_Test file for an example)
1. Import the class
2. Import `MQTTClient` from `umqtt.simple`
3. Make some variable equal `AIO_ESP(*your wifi name*,*your wifi password*,*your aio username*,*your aio key*)`

# Functions
* `connect_to_internet` - Connects the esp32 to your wifi (must either be dual band or be 2.4GHz from what I've seen) and to your aio account
* `subscribe_feed(*feed name: string*)` - Subscribes to the feed inputted, which makes `read_feed()` read it
* `register_feed(*feed name: string*,*callback function: function*)` - Connects a feed to a function, so that whenever that feed is updated, the function is called (must have only 1 parameter for the message)
* `write_feed(*feed name: string*,*message: any data type that can be converted into a string*)` - Writes a certain value onto a feed
* `read_feed()` - Creates a second thread that constantly checks for any new values on the subscribed feeds (this is done using the `_thread` library which is included in Micropython, learn more about it on [this video](https://www.youtube.com/watch?v=QeDnjcdGrpY) literally nothing is said about it on the Micropython wiki)
