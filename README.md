# AIO-Micropython
This library is a class that lets microprocessors that use Micropython (and have a wifi chip) communicate with Adafruit IO

**This library is dependant on the `umqtt.simple` library**

# How to use (Look at AIO_Micropython_Test.py for an example)
1. Import the class
2. Import `MQTTClient` from `umqtt.simple`
3. Make an instance object formatted like so:
   ```
   *instance object*=AIO_ESP(
   	*your wifi name*, # string
   	*your wifi password*, # string
   	*your aio username*, # string
   	*your aio key*, # string
   	*client id name* # string, this one is optional, and is set to ESP32 by default
   )
   ```

# Functions
* `connect_to_internet` - Connects the microprocessor to your wifi (must either be dual band or be 2.4GHz from what I've tested) and to your aio account
* `subscribe_feed` - Subscribes to the feed inputted, which makes `read_feed` read it.  
  It has 1 parameter, the feed name which is a string, so to subscribe to the feed `temp` it would be written as `*instance object*.subscribe_feed("temp")`
* `register_feed` - Connects a feed to a function, so that whenever that feed is updated, the function is called (must have only 1 parameter for the message)  
  It has 2 parameters, the feed name, which is a string, and the function that you wanted to connect to it, so if you wanted to set `temp_callback` to be the callback function for `temp`, it would be written as `*instance object*.register_feed("temp",temp_callback`
* `write_feed` - Writes a certain value onto a feed.  
  It has 2 parameters, the feed name which is a string, and the message, which can be any data type that can be converter into a string, so if you wanted the feed `temp` to equal to 5, then it would be written as `*instance_object*.write_feed("temp",5)`
* `read_feed()` - Creates a second thread that constantly checks for any new values on the subscribed feeds (this is done using the `_thread` library which is included in Micropython, learn more about it on [this video](https://www.youtube.com/watch?v=QeDnjcdGrpY) literally nothing is said about it on the Micropython wiki).  
  This has no parameters
