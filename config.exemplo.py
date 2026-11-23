# config.exemplo.py - MODELO de configuração (valores falsos)
#
# Como usar:
#   1. Copie este arquivo com o nome config.py
#   2. Preencha com os dados da SUA rede
#   3. Salve o config.py DENTRO da placa (Thonny: Salvar como -> Dispositivo MicroPython)
#
# O config.py verdadeiro NUNCA vai para o GitHub (está no .gitignore)

# ===== Wi-Fi =====
WIFI_NOME = "NOME_DA_SUA_REDE"            # Nome da rede (SSID)
WIFI_SENHA = "SENHA_DA_SUA_REDE"          # Senha da rede

# ===== IP fixo da placa na rede local =====
IP_FIXO = "192.168.1.200"                 # Endereço que a placa vai usar
MASCARA = "255.255.255.0"                 # Máscara de rede (a mais comum em casa)
GATEWAY = "192.168.1.1"                   # IP do roteador
DNS = "8.8.8.8"                           # Servidor DNS (8.8.8.8 = Google)
