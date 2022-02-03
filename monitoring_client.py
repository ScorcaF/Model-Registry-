#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from datetime import datetime
from MyMQTT import MyMQTT
from DoSomething import DoSomething
import time

class AlertReceiver(DoSomething):
    
    def __init__(self, clientID):
        self.clientID = clientID
        self.myMqttClient = MyMQTT(self.clientID, "test.mosquitto.org", 1883, self)

    def notify(self, topic, msg):
        input_json = json.loads(msg)
        
        date = datetime.fromtimestamp(input_json["bt"])
        
        records = input_json["e"]
        
        quantity = records[0]["n"]
        predicted = float(records[0]["v"])
        measure_unity = records[1]["u"]
        actual = float(records[1]["v"])
                        
        
        print('({:}/{:}/{:} {:}:{:}:{:}) {:} Alert: Predicted={:.1f}{:} Actual={:}{:}'.format(
        date.day, date.month, date.year, date.hour, date.minute, date.second, quantity, predicted,measure_unity, actual, measure_unity))
        

        
if __name__=="__main__":      
    test = AlertReceiver("alert receiver 1")
    test.run()
    test.myMqttClient.mySubscribe("/290091/alert")

    while True:
        time.sleep(1)


# In[2]:


import paho.mqtt.client as PahoMQTT


class MyMQTT:
    def __init__(self, clientID, broker, port, notifier):
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID

        self._topic = ""
        self._isSubscriber = False

        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, False) 

        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
        print ("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        # A new message is received
        self.notifier.notify (msg.topic, msg.payload)

    def myPublish (self, topic, msg):
        # if needed, you can do some computation or error-check before publishing
        print ("publishing '%s' with topic '%s'" % (msg, topic))
        # publish a message with a certain topic
        self._paho_mqtt.publish(topic, msg, 2)

    def mySubscribe (self, topic):
        # if needed, you can do some computation or error-check before subscribing
        print ("subscribing to %s" % (topic))
        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2)

        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic

    def start(self):
        #manage connection to broker
        self._paho_mqtt.connect(self.broker , self.port)
        self._paho_mqtt.loop_start()

    def stop (self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber 
            self._paho_mqtt.unsubscribe(self._topic)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()


# In[ ]:


class DoSomething():
    def __init__(self, clientID):
        # create an instance of MyMQTT class
        self.clientID = clientID
        self.myMqttClient = MyMQTT(self.clientID, "test.mosquitto.org", 1883, self)

    def run(self):
        # if needed, perform some other actions befor starting the mqtt communication
        print ("running %s" % (self.clientID))
        self.myMqttClient.start()

    def end(self):
        # if needed, perform some other actions befor ending the software
        print ("ending %s" % (self.clientID))
        self.myMqttClient.stop ()

    def notify(self, topic, msg):
        # manage here your received message. You can perform some error-check here
        print ("received '%s' under topic '%s'" % (msg, topic))

