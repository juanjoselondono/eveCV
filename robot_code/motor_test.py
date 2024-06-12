import time
from motors_setup import forward, reverse, left_turn, right_turn


# Simple Motor Test Loop 
try:
  while True:
    print('forward')
    forward(2)  # Move forward for 2 seconds
    time.sleep(2)  # Wait for 2 seconds
    print('backward')   
    reverse(2)  # Move backward for 2 seconds
    time.sleep(2)  # Wait for 2 seconds
    print('left')    
    left_turn(1)  # Turn left for 1 second    
    time.sleep(2)  # Wait for 2 seconds
    print('right')    
    right_turn(1)  # Turn right for 1 second
    time.sleep(2)  # Wait for 2 seconds
except KeyboardInterrupt:
  # Detener el bucle de eventos de MQTT y desconectarse al recibir la interrupción del teclado (commented out)
  # client.loop_stop()
  # client.disconnect()
  gpio.cleanup()
