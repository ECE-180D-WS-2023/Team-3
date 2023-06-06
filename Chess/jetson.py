import paho.mqtt.client as mqtt
import time
import serial


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/central/move")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
    client.loop_stop()

# The default message callback.
# (won't be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    if (message.topic == "ece180d/central/move"):
        serial_port.write(message.payload + b'\n')



client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

#serial_port = serial.Serial("PORT NAME HERE", baudrate=115200)
time.sleep(0.2)

while(True):
    continue
