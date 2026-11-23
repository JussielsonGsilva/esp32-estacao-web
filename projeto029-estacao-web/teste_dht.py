# Projeto 029 - Teste 3: lê o DHT11 a cada 2 segundos e mostra no Shell

import dht                                # Biblioteca do DHT (já vem no MicroPython)
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(13))               # DHT11 no pino D13

while True:
    try:
        sensor.measure()                  # Pede uma nova leitura ao sensor
        temp = sensor.temperature()       # Temperatura em °C
        umid = sensor.humidity()          # Umidade em %
        print("Temperatura:", temp, "C | Umidade:", umid, "%")
    except OSError:                       # O sensor não respondeu?
        print("Falha na leitura: confira o fio do DATA no D13")
    sleep(2)                              # O DHT11 só aceita 1 leitura a cada ~1 segundo