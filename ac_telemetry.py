from socket import *
from struct import pack, unpack
import time
import math
import serial
import threading


# Constants
HANDSHAKE = 0
SUBSCRIBE_UPDATE = 1
DISMISS = 3
AC_SERVER_IP = "127.0.0.1"
AC_SERVER_PORT = 9996

maxG=2
filter=0.2

def sendSignal(opId):
    print("Sending signal: ",opId)
    message = pack('<iii', 1, 1, opId)
    clientSocket.sendto(message, (AC_SERVER_IP, AC_SERVER_PORT))
    time.sleep(1)


def extractHandShakeRes(index, res):
    carName = res.decode('utf-16')[0: 49]
    carName = carName[0: carName.find('%')]
    driverName = res.decode('utf-16')[50: 100]
    driverName = driverName[0: driverName.find('%')]
    return (carName, driverName)

def formattedForce(value):
     currentValue= min(max(value,-maxG),maxG)
     currentValue = currentValue * (1 - filter)
     currentValue = round(currentValue * 100)/100
     return currentValue

def adruinoWrite(force):
     force = round(force, 1)
     position = force * 1000
     position = round(position, 1)
     position = str(position) + "\n"
     position = position.encode()
     adruinoSerial.write(position)
    
def combinedForce(frontalG, verticalG):
    sum = frontalG + verticalG
    netForce = 0
    if(sum == 0):
        netForce =  0
    else:
        resultant = math.hypot(frontalG, verticalG) 
        netForce = resultant if sum > 0 else -resultant 
    return netForce

#Socket connection
while True:
    try:
        print("Intializing AC Server connection")
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        print("AC Server connection established")
        time.sleep(1)
        break
    except Exception as e:
        print("AC Server connection failed", e)
        time.sleep(1)
        
#Adruino connection
while True:
    try:
        print("Intializing Adruino connection")
        adruinoSerial = serial.Serial("COM9", 115200)
        print("Adruino connection connection established")
        time.sleep(1)
        break
    except Exception as e:
        print("Adruino connection connection failed", e)
        time.sleep(1)

  
while True:
    try:
        # Send Handshake
        sendSignal(HANDSHAKE)
        time.sleep(1)
        
        response, ipAddress = clientSocket.recvfrom(500)
        (res, ) = unpack('408s', response)

        (carName,driverName) = extractHandShakeRes(0, res)
        print(f"{driverName} connected in {carName} ")

        # Send Update
        sendSignal(SUBSCRIBE_UPDATE)
        time.sleep(1)

        while True:
            response, ipAddress = clientSocket.recvfrom(500)
            pktformat = "c3xI3f6?3f4I5fIf4f4f4f4f4f4f4f4f4f4f4f4f4f4fff3f"
            unpackedData = unpack(pktformat, response)
                
            accG_horizontal =  unpackedData[11]
            accG_vertical = unpackedData[12]
            accG_frontal = unpackedData[13]

            # Calculate combined force
            combinedForces = combinedForce(accG_vertical, accG_frontal) 
            print(combinedForces) 
            combinedForces = formattedForce(combinedForces)
            print(combinedForces)    
            # Send to adruino
            if abs(combinedForces) > 0.2:    
                adruinoWrite(combinedForces)

    except Exception as e:
        print("Handshake failed", e)
