# ds1302.py - Módulo (driver) do relógio DS1302 | CLK=D25, DAT=D33, RST=D32

from machine import Pin
from time import sleep_us

# --- Pinos ---
clk = Pin(25, Pin.OUT, value=0)           # CLK: o ritmo
dat = Pin(33, Pin.OUT, value=0)           # DAT: os dados (entrada e saída)
rst = Pin(32, Pin.OUT, value=0)           # RST: liga/desliga a conversa

# --- Conversões BCD ---
def bcd_para_num(valor):
    return (valor >> 4) * 10 + (valor & 0x0F)        # Dezena * 10 + unidade

def num_para_bcd(numero):
    return ((numero // 10) << 4) | (numero % 10)     # Dezena em cima, unidade embaixo

# --- Envia 1 byte, começando pelo bit da direita ---
def enviar_byte(valor):
    dat.init(Pin.OUT)                     # DAT vira SAÍDA
    for i in range(8):
        dat.value((valor >> i) & 1)       # Coloca o bit i no fio
        sleep_us(1)
        clk.value(1)                      # O chip lê na subida
        sleep_us(1)
        clk.value(0)

# --- Recebe 1 byte ---
def receber_byte():
    dat.init(Pin.IN)                      # DAT vira ENTRADA
    valor = 0
    for i in range(8):
        valor = valor | (dat.value() << i)   # Lê o bit e encaixa na posição i
        clk.value(1)                      # Pede o próximo bit
        sleep_us(1)
        clk.value(0)
        sleep_us(1)
    return valor

# --- Grava um valor num endereço ---
def gravar(comando, valor):
    rst.value(1)                          # Liga a conversa
    enviar_byte(comando)                  # Onde gravar
    enviar_byte(valor)                    # O que gravar
    rst.value(0)                          # Desliga a conversa

# --- Lê um valor de um endereço ---
def ler(comando):
    rst.value(1)
    enviar_byte(comando)                  # De onde ler
    valor = receber_byte()                # A resposta
    rst.value(0)
    return valor

# --- Grava data e hora (ano com 2 dígitos; dia da semana 1=domingo ... 7=sábado) ---
def acertar(ano, mes, dia, dia_semana, hora, minuto, segundo):
    gravar(0x8E, 0x00)                    # Desliga a proteção contra gravação
    gravar(0x80, num_para_bcd(segundo))   # Bit CH = 0 -> relógio anda
    gravar(0x82, num_para_bcd(minuto))
    gravar(0x84, num_para_bcd(hora))      # Modo 24 horas
    gravar(0x86, num_para_bcd(dia))
    gravar(0x88, num_para_bcd(mes))
    gravar(0x8A, dia_semana)
    gravar(0x8C, num_para_bcd(ano))
    gravar(0x8E, 0x80)                    # Liga a proteção de novo

# --- Lê data e hora: devolve (ano, mes, dia, dia_semana, hora, minuto, segundo) ---
def ler_relogio():
    s = bcd_para_num(ler(0x81) & 0x7F)    # Máscara tira o bit CH
    m = bcd_para_num(ler(0x83))
    h = bcd_para_num(ler(0x85) & 0x3F)    # Máscara tira os bits de modo 12/24h
    d = bcd_para_num(ler(0x87))
    me = bcd_para_num(ler(0x89))
    ds = ler(0x8B) & 0x07                 # Dia da semana (1 a 7)
    a = bcd_para_num(ler(0x8D))
    return a, me, d, ds, h, m, s