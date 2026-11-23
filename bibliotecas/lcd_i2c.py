# ============================================================
# lcd_i2c.py — Driver do LCD 16x2 com módulo I2C (PCF8574)
# Feito no projeto 021. Use com: from lcd_i2c import *
# ============================================================

from machine import Pin, I2C
from time import sleep_ms, sleep_us

# --- Barramento I2C (SDA = D21, SCL = D22) e endereço do módulo ---
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
ENDERECO = 0x27

# --- Bits de controle dentro do byte enviado ao PCF8574 ---
RS = 0b00000001                # 0 = comando, 1 = letra
E = 0b00000100                 # Pulso de leitura
LUZ = 0b00001000               # Luz de fundo ligada

# --- Manda um byte para o chip, pelo I2C ---
def escrever_chip(valor):
    i2c.writeto(ENDERECO, bytes([valor]))

# --- Envia 4 bits de dados, com o pulso no E ---
def enviar_4bits(valor, modo):
    byte = (valor << 4) | LUZ | modo
    escrever_chip(byte | E)
    sleep_us(1)
    escrever_chip(byte)
    sleep_us(100)

# --- Envia um byte em duas metades ---
def enviar_byte(valor, modo):
    enviar_4bits(valor >> 4, modo)
    enviar_4bits(valor & 0x0F, modo)

# --- Envia um comando ---
def comando(valor):
    enviar_byte(valor, 0)
    sleep_ms(2)

# --- Escreve um texto a partir da posição atual ---
def escrever(texto):
    for letra in texto:
        enviar_byte(ord(letra), RS)

# --- Escreve um caractere pelo CÓDIGO (útil para os personalizados, 0 a 7) ---
def escrever_codigo(codigo):
    enviar_byte(codigo, RS)

# --- Move o cursor: coluna (0 a 15), linha (0 ou 1) ---
def posicionar(coluna, linha):
    endereco = coluna if linha == 0 else 0x40 + coluna
    comando(0x80 | endereco)

# --- Limpa a tela ---
def limpar():
    comando(0x01)

# --- Cria um caractere personalizado (posição 0 a 7, desenho de 8 linhas de 5 bits) ---
def criar_caractere(posicao, desenho):
    comando(0x40 | (posicao << 3))       # Vai para a memória de desenhos (CGRAM)
    for linha in desenho:
        enviar_byte(linha, RS)           # Grava as 8 linhas do desenho
    comando(0x80)                        # Volta para a tela

# --- Inicialização (sequência do manual) ---
def iniciar():
    sleep_ms(50)
    enviar_4bits(0x03, 0)
    sleep_ms(5)
    enviar_4bits(0x03, 0)
    sleep_ms(1)
    enviar_4bits(0x03, 0)
    enviar_4bits(0x02, 0)
    comando(0x28)                        # 4 bits, 2 linhas
    comando(0x0C)                        # Tela ligada, sem cursor
    comando(0x06)                        # Cursor anda para a direita
    limpar()