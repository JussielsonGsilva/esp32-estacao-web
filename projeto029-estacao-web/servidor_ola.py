# Projeto 029 - Teste 2: servidor web simples (página fixa)

import network                            # Rede
import socket                             # Socket: a "tomada de rede"
from time import sleep
import config                             # Nosso config.py (senha fica só na placa)

# ===== 1) CONECTAR NO WI-FI =====
wifi = network.WLAN(network.STA_IF)       # Modo cliente
wifi.active(True)                         # Liga o rádio
wifi.ifconfig((config.IP_FIXO, config.MASCARA, config.GATEWAY, config.DNS))   # IP fixo

if not wifi.isconnected():
    wifi.connect(config.WIFI_NOME, config.WIFI_SENHA)   # Conecta
    while not wifi.isconnected():         # Espera conectar
        sleep(1)

ip = wifi.ifconfig()[0]                   # Pega o IP
print("Conectado! Abra no navegador: http://" + ip)

# ===== 2) A PÁGINA (o texto que vamos devolver) =====
PAGINA = """HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head><title>ESP32</title></head>
<body>
<h1>Olá! Eu sou o ESP32 do Jussielson</h1>
<p>Este é o meu primeiro servidor web.</p>
</body>
</html>
"""
# As aspas triplas (""") permitem um texto de várias linhas

# ===== 3) ABRIR A PORTA 80 =====
servidor = socket.socket()                # Cria o socket
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # Deixa reusar a porta ao rodar de novo
servidor.bind(("0.0.0.0", 80))            # Escuta na porta 80, em qualquer IP da placa
servidor.listen(1)                        # Aceita 1 visitante por vez na fila
print("Servidor esperando visitas...")

# ===== 4) ATENDER AS VISITAS =====
while True:
    cliente, endereco = servidor.accept() # ESPERA alguém conectar (o programa para aqui)
    print("Visita de:", endereco[0])      # Mostra o IP de quem abriu a página
    pedido = cliente.recv(1024)           # Lê o pedido do navegador (até 1024 bytes)
    cliente.send(PAGINA)                  # Envia a resposta (cabeçalho + HTML)
    cliente.close()                       # Fecha a conexão com esse visitante