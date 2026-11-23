# Projeto 029 - Teste 1: conecta no Wi-Fi usando o config.py da placa

import network                            # Biblioteca de rede do MicroPython
from time import sleep
import config                             # Nosso config.py (senha fica só dentro da placa)

wifi = network.WLAN(network.STA_IF)       # STA = "estação": a placa se conecta a um roteador
wifi.active(True)                         # Liga o rádio Wi-Fi

# Usa o IP fixo: (IP, máscara, gateway, DNS)
wifi.ifconfig((config.IP_FIXO, config.MASCARA, config.GATEWAY, config.DNS))

if not wifi.isconnected():                # Ainda não está conectado?
    print("Conectando na rede", config.WIFI_NOME, "...")
    wifi.connect(config.WIFI_NOME, config.WIFI_SENHA)   # Envia nome e senha ao roteador

    tentativas = 0
    while not wifi.isconnected() and tentativas < 20:   # Espera até 20 segundos
        print(".", end="")                # Mostra um ponto a cada segundo (end="" = sem pular linha)
        sleep(1)
        tentativas += 1
    print()                               # Pula a linha depois dos pontos

if wifi.isconnected():
    print("Conectado!")
    print("IP da placa:", wifi.ifconfig()[0])   # [0] = o primeiro item da tupla, o IP
else:
    print("Nao conectou. Confira se o roteador esta ligado e perto da placa.")