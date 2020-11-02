#!/usr/bin/env python3

# Temp_2.py
# More information to be added here

from ds18b20 import DS18B20	
import time
import paho.mqtt.client as mqtt

def recon():
    global debug
    try:
        mqttc.reconnect()
        if debug:
            print('Successfull reconnected to the MQTT server')
        topic_subscribe()
    except:
        if debug:
            print('(recon) Could not reconnect to the MQTT server. Trying again in 10 seconds')

def on_connect(client, userdata, flags, rc):
    global debug
    if rc==0:
        mqttc.connected_flag=True #set flag
        print("Connected OK")
    else:
        print("Bad connection Returned code=",rc)

    # set connection status to ON in topic - this will be set to OFF by disconnect or last will
    publish_message(msg="ON", mqtt_path='system/connectionstatus/raspberrypi2', mqtt_qos=2, mqtt_retain=True)
    if debug:
        print("Connected With Result Code {}".format(rc))


def on_disconnect(client, userdata, rc):
    global debug
    # set connection status to OFF in topic - this will be set to ON by on_connect
    publish_message(msg="OFF", mqtt_path='system/connectionstatus/raspberrypi2', mqtt_qos=2, mqtt_retain=True)
    if rc != 0:
        if debug:
            print('Unexpected disconnection from MQTT, trying to reconnect')
        recon()

def connect(mqttc):
    global debug
    try:
        #mqttc.connect('10.100.100.210', port=1883, keepalive=60)
        mqttc.connect('192.168.188.42', port=1883, keepalive=60)
        if debug:
           print('Connecting...In wait loop')
        time.sleep(1)
    except:
        if debug:
            print('(connect) Could not connect to the MQTT server. Trying again in 10 seconds')
        time.sleep(10)
        connect(mqttc)

def publish_message(msg, mqtt_path, mqtt_qos, mqtt_retain):
    global debug
    mqttc.publish(mqtt_path, payload=msg, qos=mqtt_qos, retain=mqtt_retain)
    time.sleep(0.1)
    if debug:
        print('published message {0} on topic {1} with QoS {2} and retain {3} at {4}'.format(msg, mqtt_path, mqtt_qos, mqtt_retain, time.asctime(time.localtime(time.time()))))


#debug = False
debug = True

#Connect to the MQTT broker
mqttc = mqtt.Client('raspberrypi2')
#mqttc.username_pw_set(username="openhab",password="<ENTER_PASSWORD_HERE>")
#mqttc.username_pw_set(username='', password='')


#Define the mqtt callbacks
mqttc.on_connect = on_connect
#mqttc.on_message = on_message
mqttc.on_disconnect = on_disconnect
# set connection status to OFF in topic - this will be set to ON by on_connect

mqttc.will_set("system/connectionstatus/raspberrypi2", payload="OFF", qos=2, retain=True)

# Connect to the MQTT server
if debug:
        print("Connecting to MQTT server...")
connect(mqttc)
time.sleep(1)

mqttc.loop_start()

time.sleep(1)

	
# test temperature sensors
x = DS18B20()
count=x.device_count()

while True:
       i = 0
       while i < count:
              print(x.tempC(i))
              #post data to mqtt broker
              publish_message(msg=x.tempC(i)[0],mqtt_path='raspberrypi2/temp/' + x.tempC(i)[1],mqtt_qos=2,mqtt_retain=True)
              i += 1
       time.sleep(60)

