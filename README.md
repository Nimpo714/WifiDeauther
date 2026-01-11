## Это скрипт для деаутентификации пользователей от сети wifi
# Установка на Arch Linux

```bash
yay -S aircrack-ng mdk4 git
git clone https://github.com/Nimpo714/WifiDeauther
cd WifiDeauther
sudo python deauther.py
```

# Библеотеки
```bash
yay -S python-uv
uv venv
source .venv/bin/activate
uv pip install rich 
```

Чтобы собрать с использованием pyinstaller
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --console --name "WifiDeauther" --version-file "1.1" --uac-admin --hidden-import "subprocess" --hidden-import "rich"  "deauther.py"
```

# Примечания
- При использовании скрипта есть шанс что вы от ключитесь от wifi
- Скрипт необходимо запускать от рута
- Если вы перезапустили скрипт и в Доступных Сетевых интерфейсах есть например wlan0mon то введите просто wlan0 
- Если вам нужно использовать данный сетевой интерфейс после скрипта используйте sudo airmon-ng stop <ваш сетевой интерфейс>

# License GPL-3.0
