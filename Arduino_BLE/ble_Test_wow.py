import sys
import time
import binascii
import struct
from bluepy import btle
from bluepy.btle import UUID, Peripheral

def main():
	if len(sys.argv) != 2:
		print("Fatal, must pass device address:", sys.argv[0], "<device address="">")
		quit()
		
	accelServiceUuid = "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
	accCharUuid = "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
	
	print("Connecting......", accelServiceUuid)
	peripheralObject = btle.Peripheral(sys.argv[1])

	print("Services...")
	for svc in peripheralObject.services:
		print(str(svc))

	mySensor = btle.UUID(accelServiceUuid)
	sensorService = peripheralObject.getServiceByUUID(mySensor)
	
	print("get Characteristics...")
	accVal = sensorService.getCharacteristics(accCharUuid)[0]
	
	while 1:
		print(parseFloatData(accVal.read()))
		
def parseFloatData(data):
	data = binascii.b2a_hex(data)
	data = binascii.unhexlify(data)

	# print(data)
	info = [data[i:i+4] for i in range (0, len(data), 4)]

	ans = struct.unpack('<f', info[0]) + struct.unpack('<f', info[1]) + struct.unpack('<f', info[2]) + struct.unpack('<f', info[3]) + struct.unpack('<f', info[4]) + struct.unpack('<f', info[5]) 
	return ans
	


if __name__ == "__main__":
    main()