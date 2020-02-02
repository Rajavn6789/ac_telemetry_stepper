import serial
import time
import random
import serial.tools.list_ports

adruinoSerial = serial.Serial("COM9", 115200)
time.sleep(2)
print("Adruino serial connection established")

def adruinoWrite(force):
     force = round(force, 1)
     position = force * 1000
     position = round(position, 1)
     position = str(position) + "\n"
     position = position.encode()
     adruinoSerial.write(position)

while True:
    longitudinalG = (round(random.uniform(-1, 1), 1))
    if(abs(longitudinalG) >= 0.3):
       adruinoWrite(longitudinalG)
