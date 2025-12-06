esptool --port COM6 erase_flash

esptool --port COM6 --baud 460800 write_flash 0x1000 ESP32_GENERIC-20250911-v1.26.1.bin

ampy --port COM6 put src/main.py