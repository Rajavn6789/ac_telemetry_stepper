import serial
import time
import random

adruinoSerial = serial.Serial("COM9", 115200, timeout=1000)
time.sleep(2)
print("Adruino serial connection established")

def adruinoWrite(force):
     force = round(force, 1)
     position = force * 2000
     position = round(position, 1)
     position = str(position) + "\n"
     position = position.encode()
     print(position)
     adruinoSerial.write(position)

while True:

     longitudinalG = (round(random.uniform(-2, 2), 1))
     if(abs(longitudinalG) >= 0.2):
          adruinoWrite(longitudinalG)

     # position = adruinoSerial.readline()
     # position = position.decode()  # decode byte string into Unicode  
     # position = position.rstrip()
     # print(position)     
