import serial
import time
## Vars ################
port = "COM6"
baud = 9600
########################
## Command components ???
startFlag = bytes.fromhex("A5")
moduleAddress = bytes.fromhex("40")
commandID = bytes.fromhex("96")
dataLength = bytes.fromhex("08")
data = bytes.fromhex("00" * 8)  
checksum = 0
_cmd = startFlag + moduleAddress + commandID + dataLength + data

# calc checksum - guess 1
for b in _cmd:
    checksum += b

# get low bytes only # CHECKING IF CHECKSUM IS  OR 255
checksum = checksum & 0xff

# convert to hex
checksum = f"{checksum:02X}" # creating a string and defining hexadecimel string format
checksum = bytes.fromhex(checksum) 


print(f"checksum: {checksum}")

cmd = _cmd + checksum + b"\n"
print (f"sending command {cmd}")

with serial.serial_for_url(port, baud) as s:
    s.timeout = 1
    s.write_timeout = 1
    s.flushInput()
    s.flushOutput()
    bytes_written = s.write(cmd)
    print (f"wrote {bytes_written} bytes")

    response_line = s.readline()
    #time.sleep(2)
    print (f"Got response: {response_line}")
    '''for _ in range(10):
        response_line = s.readline()
        #time.sleep(2)
        print (f"Got response: {response_line}")'''
