#!/usr/bin/python
import sys
import time
import os
import string
import random
import dbus
import paho.mqtt.client as mqtt

def read_credentials_file(filename):
    f = open(filename)
    return f.readline().strip(), f.readline().strip()

mqtt_server = "devaamo.fi"
mqtt_port = 1883
mqtt_keepalive = 210
# Note: getting the will wrong will make your connection fail authentication!
mqtt_set_will = False
mqtt_credentials = os.path.expanduser("~/.nuntius_auth")
mqtt_user, mqtt_password = read_credentials_file(mqtt_credentials)
mqtt_topic_base = "sailfish/"+mqtt_user+"/"
mqtt_name = "sailfish_"+mqtt_user

print "starting nuntius!"
print "Press CTRL + C to exit"

def on_log(mosq, obj, level, string):
    print(string)

def subscribe(mosq):
    mqttc.subscribe("sailfish/broadcast/#", 2)

def on_connect(mosq, userdata, rc):
    if rc == 0:
        print("Connected to Trusor: "+mqtt_server)
        subscribe(mosq)
        if mqtt_set_will: mqttc.publish(mqtt_topic_base+"nuntius/state", "connected", 2, True)
    else:
        print("Connection failed with error code: "+str(rc))

def on_message(mosq, obj, msg):
    print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)

mqttc = mqtt.Client(mqtt_name, False, None, mqtt.MQTTv311 )

mqttc.username_pw_set(mqtt_user, mqtt_password)
mqttc.on_log = on_log
mqttc.on_connect = on_connect
if mqtt_set_will: mqttc.will_set(mqtt_topic_base+"nuntius/state", None, 2, True)
mqttc.connect(mqtt_server, mqtt_port, mqtt_keepalive)
mqttc.on_message = on_message



bus = dbus.SessionBus()


mqttc.loop_forever()

