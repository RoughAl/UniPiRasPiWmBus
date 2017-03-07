#!/usr/bin/env python
import binascii
import time
import sqlite3
#import serial
#import os
import sys, getopt

############### Vypocitani VendorID z M-Pole ###########################################################################

def get_vendor_name(vendor_input):
    vendor_hex1 = vendor_input[2:4]
    vendor_hex2 = vendor_input[0:2]
    vendor_bin1 = bin(int(vendor_hex1, 16))[2:]
    vendor_bin2 = bin(int(vendor_hex2, 16))[2:]
    vendor_bin1 = vendor_bin1[0:8].zfill(7)
    vendor_bin2 = vendor_bin2[0:8].zfill(8)
    vendor_binary = vendor_bin1 + vendor_bin2
    vendor_letter1 = vendor_binary[0:5].zfill(5)
    vendor_letter2 = vendor_binary[5:10].zfill(5)
    vendor_letter3 = vendor_binary[10:15].zfill(5)
    vendor_char1 = int(vendor_letter1, 2) + 64
    vendor_char2 = int(vendor_letter2, 2) + 64
    vendor_char3 = int(vendor_letter3, 2) + 64
    znak1 = chr(vendor_char1)
    znak2 = chr(vendor_char2)
    znak3 = chr(vendor_char3)
    return znak1+znak2+znak3

############### Demonstracni hodnoty telegramu pro offline ukazku ci testy #############################################

def get_demo_telegrams():
    words = []
    # WEPTECH AES
    words.append("32002E44B05C10000000021B7A2B082005AC68E7F50EE6507BBE2D9F219C4F628B5899B9CD54239872373114E372C59E817DCF")  # ME
    words.append("32002E44B05C10000000021B7A2C0820051D2B70A744ACD71B237CF8F6C54C1A7A2E0DE2F24C9225E4BB0FB278C8A68CF77985")  # ME
    words.append("32002E44B05C10000000021B7A2D0820058FBFB2CE35F67F9F66E00E751BBBF5271E07F63C09BBAA77CDA574D6A0D672477C6E")  # ME
    # WEPTECH CLEAN
    words.append("32002E44B05C11000000021B7A920800002F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F1234")  # KZ
    words.append("32002e44b05c10000000021b7a660800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")  # ME
    # BONEGA AES
    words.append("22001E44EE092101000001067A4F0010051AB94C4FDA694309E347E86FA437790C1234")  # KZ
    words.append("22001E44EE092101000001077A43001005C8C16D2F1F1DBDD884515FC9E4905B357C9C")  # ME
    words.append("22001E44EE092101000001067A430010051DBBA0F32262EBC81D9AF8F70CB8FB7E6ED5")  # ME
    words.append("22001E44EE092101000001077A44001005D3CCF20F690F2A9F3E6C6DC5CC32429F760C")  # ME
    words.append("22001E44EE092101000001067A440010055A5E995023C09D3756726C09C57B5DE27621")  # ME
    words.append("22001E44EE092101000001077A4500100578261B54AC056DC59A34EFABB7680580794A")  # ME
    # KAMSTUP AES
    words.append("00005E442D2C9643636013047AD21050052F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F1234")  # AH
    # ZPA
    words.append("00002A44016A4493671201027244936712016A01020000002086108300762385010000862083009731920000001234")  # KZ
    # PIKKERTON
    words.append("000028442B414452127002027A3500000004FB2CCDC3000001FD49E002FD591A01022B200004035C0000001234")  # KZ
    # TECHEM
    words.append("000032446850633481346980A0919F1DF800D0282901600CAE0C152000343A392328060000000000000000000000000000000000001234")  # KZ
    return words

############### Vypocitani RSSI v dBm z (-3,-4) ########################################################################

def get_signal_value(sensor_rssi):
    #print(sensor_rssi)
    sensor_rssi = int(sensor_rssi, 16)
    sensor_rssi = (sensor_rssi/2)-130
    return str(sensor_rssi)

########################################################################################################################

if 1==1:
    words = get_demo_telegrams()
else:
    words = ''



wordLed = len(words)
for i in range(0, wordLed):
    parsedstring = str(words[i])
    sensor_sn = parsedstring[18:20] + parsedstring[16:18] + parsedstring[14:16] + parsedstring[12:14]
    sensor_ver = parsedstring[20:22]
    sensor_type = parsedstring[22:24]
    sensor_manu = get_vendor_name(parsedstring[8:12])

    increment = parsedstring[26:28]

    #rssi = get_signal_value(parsedstring[-2:0])
    rssi = "00"

    temperature = parsedstring[44:45].replace("0", "") + parsedstring[45:46].replace("0", "") + parsedstring[42:43] + "." + parsedstring[43:44]
    humidity = parsedstring[54:55].replace("0", "") + parsedstring[55:56].replace("0", "") + parsedstring[52:53] + "." + parsedstring[53:54]


    if parsedstring[64:66] == "01": errors = "Sabotaz cidla"
    if parsedstring[66:68] == "01": errors = "Vybita baterie"

    print(time.strftime("%H:%M:%S %d/%m/%Y") + "    Mereni: " + increment + "   Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + get_signal_value(rssi) + "dB    Teplota: " + temperature + "C    Vlhkost: " + humidity + "%")

conn = sqlite3.connect('MainDatabase.db')
print("Opened database successfully")

conn.close()

