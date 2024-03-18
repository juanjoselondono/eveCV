## MQTT Connection Stream, Bounding Box algoritm
import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

#Motor Configuration
def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
def forward(sec):
    init()
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup() 
def reverse(sec):
    init()
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()
def left_turn(sec):
    init()
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()
def right_turn(sec):
    init()
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()

# MQTT configuration
broker = '192.168.41.48' 
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
        forward(1)
    elif (received_message == "reverse"):
        reverse(1)
    elif (received_message == "left"):
        left_turn(1)
    elif (received_message == "right"):
        right_turn(1)
    
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

