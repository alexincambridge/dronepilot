import time
import os
import serial.tools.list_ports

PICO_PORT = "/dev/tty.usbmodem146401"  # Ajusta si el puerto cambia

def is_pico_connected():
    """ Verifica si la Raspberry Pi Pico está conectada """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if PICO_PORT in port.device:
            return True
    return False

while True:
    if is_pico_connected():
        print(f"Pico detectada en {PICO_PORT}.")
    else:
        print("Pico desconectada. Esperando reconexión...")

        # Reiniciar Thonny automáticamente en MacOS
        os.system("pkill -f thonny")  # Cierra Thonny si está abierto
        time.sleep(2)
        os.system("open -a Thonny")  # Vuelve a abrir Thonny

    time.sleep(5)  # Espera 5 segundos antes de verificar nuevamente