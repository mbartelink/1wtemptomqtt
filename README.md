# 1wtemptomqtt
1wire temperature sensors publish to MQTT

This code can be used to read multiple 1-wire temperature sensors and export them to an MQTT broker directly. From the MQTT broken, the data can be used anywhere, for example Openhab, Domoticz or any other service.
Each connected 1-wire temperature sensor has an unique ID and each sensor uses separate MQTT topic including the ID. This way, it is easy to separate and identify sensors.

Marwin
