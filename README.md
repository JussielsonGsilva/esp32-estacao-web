# ESP32 com MicroPython — projetos de IoT

Projetos selecionados de **IoT e Sistemas Embarcados** com ESP32 e MicroPython, desenvolvidos numa trilha de estudos do básico ao avançado.

Cada projeto tem sua própria pasta com **código comentado**, **ligações**, **fotos da montagem** e o **passo a passo** do desenvolvimento.

<p align="center">
  <img src="projeto029-estacao-web/fotos/pagina-pc.png" alt="Estação web com ESP32" width="700">
</p>

---

## Projetos publicados

| Projeto | Descrição | Tecnologias |
|---|---|---|
| [Estação Web](projeto029-estacao-web/) | Servidor web no próprio ESP32 com temperatura, umidade e hora sincronizada pela internet (NTP) num relógio RTC | Wi-Fi, HTTP, sockets, NTP, DHT11, DS1302, CSS Grid |

## Hardware e ferramentas

| Item | Detalhe |
|---|---|
| Placa | ESP32 DevKit (ESP-WROOM-32, 30 pinos) |
| Firmware | MicroPython 1.29 |
| IDE | Thonny |
| Simulação | Wokwi |
| Terminal | `mpremote` (Linux) |

## Bibliotecas próprias

| Arquivo | Descrição |
|---|---|
| [`bibliotecas/lcd_i2c.py`](bibliotecas/lcd_i2c.py) | Driver do LCD 16x2 via I2C (PCF8574), modo 4 bits |
| [`bibliotecas/ds1302.py`](bibliotecas/ds1302.py) | Driver do relógio DS1302 (protocolo de 3 fios, BCD) |

## Configuração

Os projetos que usam Wi-Fi leem as credenciais de um arquivo `config.py` **dentro da placa**, que **não é versionado**.

1. Copie [`config.exemplo.py`](config.exemplo.py) para `config.py`.
2. Preencha com os dados da sua rede.
3. Salve o `config.py` **dentro da placa** (Thonny: *Salvar como → Dispositivo MicroPython*).

## Autor

**Jussielson** — Analista e Desenvolvedor de Sistemas

[GitHub](https://github.com/JussielsonGsilva)
