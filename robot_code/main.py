## MQTT Connection Stream, Bounding Box algoritm
from motors_setup import forward, reverse, left_turn, right_turn
import paho.mqtt.client as mqtt
import time
broker = '192.168.177.48' 
topic = 'test'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Conectado al broker MQTT')
        client.subscribe(topic)
    else:
        print('Error de conexión al broker MQTT')

def on_message(client, userdata, msg):
    received_message = msg.payload.decode('utf-8')   
    print("Received message:", received_message)
    if (received_message == "forward"):
        print('forward')
        forward(1)
        time.sleep(0.2)
    elif (received_message == "reverse"):
        print('reverse')
        reverse(1)
        time.sleep(0.2)
    elif (received_message == "left"):
        print('left')
        left_turn(1)
        time.sleep(0.2)
    elif (received_message == "right"):
        print('right')
        right_turn(1) 
        time.sleep(0.2)
# Configuración y ejecución del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)

# Iniciar el bucle de eventos de MQTT
client.loop_start()
try:
    while True:
        # Realizar otras operaciones o pausar el bucle según sea necesario
        time.sleep(0.6)
except KeyboardInterrupt:
    # Detener el bucle de eventos de MQTT y desconectarse al recibir la interrupción del teclado
    client.loop_stop()
    client.disconnect()