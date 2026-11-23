# Projeto 029 - Teste 4: pega a hora certa pela internet (NTP) e mostra no Shell

import network                            # Rede
import ntptime                            # Cliente NTP (já vem no MicroPython)
import time                               # Funções de tempo
from time import sleep
import config                             # Nosso config.py (senha fica só na placa)

FUSO = -3                                 # Horas de diferença para o UTC (Brasil = -3)

# ===== 1) WI-FI =====
wifi = network.WLAN(network.STA_IF)       # Modo cliente
wifi.active(True)                         # Liga o rádio
wifi.ifconfig((config.IP_FIXO, config.MASCARA, config.GATEWAY, config.DNS))   # IP fixo

if not wifi.isconnected():
    wifi.connect(config.WIFI_NOME, config.WIFI_SENHA)
    while not wifi.isconnected():
        sleep(1)
print("Wi-Fi conectado")

# ===== 2) PERGUNTAR A HORA AO SERVIDOR NTP =====
ntptime.host = "pool.ntp.br"              # Servidores de hora oficiais do Brasil (NTP.br)

for tentativa in range(5):                # Tenta até 5 vezes (a internet pode falhar)
    try:
        ntptime.settime()                 # Pergunta a hora e acerta o relógio interno (em UTC)
        print("Hora recebida do NTP!")
        break                             # Deu certo: sai do for
    except OSError:
        print("Falha no NTP, tentando de novo...")
        sleep(2)

# ===== 3) MOSTRAR A HORA LOCAL =====
# --- FUNÇÃO: devolve a hora local (UTC + FUSO) ---
def hora_local():
    segundos = time.time() + FUSO * 3600  # time.time() = segundos em UTC; 3600 s = 1 hora
    return time.localtime(segundos)       # Converte para (ano, mês, dia, hora, min, seg, dia_sem, dia_ano)

while True:
    a, me, d, h, m, s, ds, _ = hora_local()   # Desempacota os 8 valores (o último não usamos)
    print("%02d/%02d/%04d  %02d:%02d:%02d" % (d, me, a, h, m, s))
    sleep(1)