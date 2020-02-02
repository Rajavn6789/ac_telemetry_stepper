import serial
import time
import random
import serial.tools.list_ports

adruinoSerial = serial.Serial("COM9", 115200)
time.sleep(2)
print("Adruino serial connection established")

while True:
    verticalG = (round(random.uniform(-1, 1), 1))
    if(abs(verticalG) >= 0.3):
        pos = verticalG * 2000 ;
        pos = round(pos, 1)
        pos = str(pos) + "\n"
        pos = pos.encode()
        print(verticalG, pos)
        adruinoSerial.write(pos)
        time.sleep(0.1)
