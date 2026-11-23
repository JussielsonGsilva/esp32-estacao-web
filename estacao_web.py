# Projeto 029: estação web - temperatura, umidade e data/hora (NTP + DS1302) com CSS

import network                            # Rede
import socket                             # Socket: a "tomada de rede"
import ntptime                            # Hora pela internet
import time                               # Funções de tempo
import dht                                # Sensor DHT
from machine import Pin
from time import sleep
import config                             # Nosso config.py (senha fica só na placa)
import ds1302                             # Nosso módulo do relógio (salvo na placa)

FUSO = -3                                 # Brasil = UTC -3
DIAS = ["", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]   # Nomes (posição 1 a 7)

# ===== 1) SENSOR =====
sensor = dht.DHT11(Pin(13))               # DHT11 no D13
ultima_temp = "--"                        # Último valor bom
ultima_umid = "--"

# --- FUNÇÃO: lê o sensor; se falhar, mantém o último valor bom ---
def ler_sensor():
    global ultima_temp, ultima_umid
    try:
        sensor.measure()
        ultima_temp = sensor.temperature()
        ultima_umid = sensor.humidity()
    except OSError:
        print("Falha na leitura do DHT11 (usando o ultimo valor)")
    return ultima_temp, ultima_umid

# --- FUNÇÃO: lê o DS1302 e devolve a data e a hora já como texto ---
def data_hora_texto():
    a, me, d, ds, h, m, s = ds1302.ler_relogio()
    nome = DIAS[ds] if 1 <= ds <= 7 else "???"
    data = "%s %02d/%02d/20%02d" % (nome, d, me, a)    # Ex.: Seg 23/11/2026
    hora = "%02d:%02d:%02d" % (h, m, s)                # Ex.: 11:05:30
    return data, hora

# ===== 2) WI-FI =====
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.ifconfig((config.IP_FIXO, config.MASCARA, config.GATEWAY, config.DNS))
if not wifi.isconnected():
    wifi.connect(config.WIFI_NOME, config.WIFI_SENHA)
    while not wifi.isconnected():
        sleep(1)
ip = wifi.ifconfig()[0]
print("Wi-Fi conectado:", ip)

# ===== 3) NTP -> DS1302 (uma vez, ao ligar) =====
ntptime.host = "pool.ntp.br"
for tentativa in range(5):
    try:
        ntptime.settime()                 # Acerta o relógio interno (UTC)
        a, me, d, h, m, s, ds, _ = time.localtime(time.time() + FUSO * 3600)   # Hora local
        ds1302.acertar(a % 100, me, d, (ds + 1) % 7 + 1, h, m, s)   # Grava no DS1302
        print("DS1302 acertado pela internet!")
        break
    except OSError:
        print("Falha no NTP, tentando de novo...")
        sleep(2)

# ===== 4) A PÁGINA (lembrete: no CSS as chaves são dobradas {{ }}) =====
MODELO = """HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="5">
<title>Estação ESP32</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Segoe UI", Arial, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0; min-height: 100vh; padding: 24px;
  }}
  header {{ text-align: center; margin-bottom: 28px; }}
  header h1 {{ font-size: 28px; letter-spacing: 1px; }}
  header p {{ color: #94a3b8; font-size: 14px; margin-top: 6px; }}
  .grade {{
    display: grid; gap: 18px; max-width: 900px; margin: 0 auto;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }}
  .cartao {{
    background: #1e293b; border-radius: 16px; padding: 24px;
    border-top: 4px solid var(--cor);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35); text-align: center;
  }}
  .icone {{ font-size: 34px; }}
  .titulo {{ color: #94a3b8; font-size: 14px; text-transform: uppercase; margin: 8px 0; }}
  .valor {{ font-size: 44px; font-weight: bold; color: var(--cor); }}
  .temp {{ --cor: #f97316; }}
  .umid {{ --cor: #38bdf8; }}
  .relogio {{ --cor: #a78bfa; }}
  footer {{ text-align: center; color: #64748b; font-size: 12px; margin-top: 28px; }}
</style>
</head>
<body>
<header>
  <h1>Estação ESP32</h1>
  <p>Atualiza sozinha a cada 5 segundos</p>
</header>
<main class="grade">
  <div class="cartao temp">
    <div class="icone">🌡️</div>
    <div class="titulo">Temperatura</div>
    <div class="valor">{} °C</div>
  </div>
  <div class="cartao umid">
    <div class="icone">💧</div>
    <div class="titulo">Umidade</div>
    <div class="valor">{} %</div>
  </div>
  <div class="cartao relogio">
    <div class="icone">🕒</div>
    <div class="titulo">{}</div>
    <div class="valor">{}</div>
  </div>
</main>
<footer>ESP32 • DHT11 • DS1302 • {}</footer>
</body>
</html>
"""
# Os 5 {} recebem, em ordem: temperatura, umidade, data, hora e IP

# ===== 5) SERVIDOR NA PORTA 80 =====
servidor = socket.socket()
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", 80))
servidor.listen(1)
print("Estacao no ar! Abra: http://" + ip)

# ===== 6) ATENDER AS VISITAS =====
while True:
    cliente, endereco = servidor.accept() # Espera um visitante
    try:
        pedido = cliente.recv(1024)       # Lê o pedido
        temp, umid = ler_sensor()         # Lê o sensor na hora
        data, hora = data_hora_texto()    # Lê o DS1302 na hora
        resposta = MODELO.format(temp, umid, data, hora, ip)   # Preenche os 5 {}
        cliente.send(resposta.encode())   # Envia
        print("Visita de", endereco[0], "->", temp, "C", umid, "%", hora)
    except OSError:
        print("Conexao interrompida pelo navegador")
    cliente.close()