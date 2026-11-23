# Projeto 029 - Teste 5: pega a hora pelo NTP, grava no DS1302 e lê de volta

import network                            # Rede
import ntptime                            # Cliente NTP
import time                               # Funções de tempo
from time import sleep
import config                             # Nosso config.py (senha fica só na placa)
import ds1302                             # Nosso módulo do relógio (salvo na placa)

FUSO = -3                                 # Brasil = UTC -3
DIAS = ["", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]   # Nomes (posição 1 a 7)

# ===== 1) WI-FI =====
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.ifconfig((config.IP_FIXO, config.MASCARA, config.GATEWAY, config.DNS))
if not wifi.isconnected():
    wifi.connect(config.WIFI_NOME, config.WIFI_SENHA)
    while not wifi.isconnected():
        sleep(1)
print("Wi-Fi conectado")

# ===== 2) NTP: ACERTA O RELÓGIO INTERNO (EM UTC) =====
ntptime.host = "pool.ntp.br"              # Servidores de hora do Brasil
ntp_ok = False                            # Ainda não conseguimos a hora
for tentativa in range(5):
    try:
        ntptime.settime()                 # Pergunta a hora
        ntp_ok = True                     # Deu certo
        break
    except OSError:
        print("Falha no NTP, tentando de novo...")
        sleep(2)

# ===== 3) GRAVA A HORA LOCAL NO DS1302 =====
if ntp_ok:
    a, me, d, h, m, s, ds, _ = time.localtime(time.time() + FUSO * 3600)   # Hora local
    dia_ds1302 = (ds + 1) % 7 + 1         # Converte: segunda 0 -> 2 ... domingo 6 -> 1
    ds1302.acertar(a % 100, me, d, dia_ds1302, h, m, s)   # a % 100: 2026 -> 26
    print("DS1302 acertado pela internet!")
else:
    print("Sem NTP: o DS1302 continua com a hora que ja tinha")

# ===== 4) LÊ O DS1302 A CADA SEGUNDO =====
while True:
    a, me, d, ds, h, m, s = ds1302.ler_relogio()   # Lê direto do chip
    nome = DIAS[ds] if 1 <= ds <= 7 else "???"
    print("DS1302: %s %02d/%02d/20%02d  %02d:%02d:%02d" % (nome, d, me, a, h, m, s))
    sleep(1)