## MQTT Connection Stream, Bounding Box algoritm
from motors_setup import forward, reverse, left_turn, right_turn
import paho.mqtt.client as mqtt
import time
import json
import threading

broker = '192.168.27.48'
topic = 'test'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
        client.subscribe(topic, qos=0)
    else:
        print('Error connecting to MQTT broker')

def handle_motor_commands(horizontal_position, distance):
    if distance == "Far":
        print('Forward')
        forward(0.2)
        time.sleep(0.5)
    elif distance == "Close":
        print('Reverse')
        reverse(0.2)
        time.sleep(0.5)
    elif horizontal_position == "Left":
        print('Left')
        left_turn(0.2)
        time.sleep(0.5)
    elif horizontal_position == "Right":
        print('Right')
        right_turn(0.2)
        time.sleep(0.5)
    else:
        print('Other')

def on_message(client, userdata, msg):
    received_message = msg.payload.decode('utf-8')

    # Check and fix the format if necessary
    if received_message.startswith("{'") and received_message.endswith("'}"):
        received_message = received_message.replace("'", '"')
    
    try:
        received_message = json.loads(received_message)
        print("Received message:", received_message)
        print("Type:", type(received_message))  # This should print <class 'dict'>
        
        horizontal_position = received_message.get('horizontal_position')
        distance = received_message.get('distance')

        # Create a new thread to handle motor commands
        motor_thread = threading.Thread(target=handle_motor_commands, args=(horizontal_position, distance))
        motor_thread.start()
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# MQTT client configuration and execution
client = mqtt.Client(clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)

# Start the MQTT client event loop
client.loop_start()

try:
    while True:
        # Perform other operations or pause the loop as necessary
        time.sleep(0.6)
except KeyboardInterrupt:
    # Stop the MQTT client event loop and disconnect on keyboard interruption
    client.loop_stop()
    client.disconnect()


