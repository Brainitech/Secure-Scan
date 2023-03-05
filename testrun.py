import serial
from datetime import datetime
curr = datetime.now()
time = curr.strftime("%H:%M:%S")

ser = serial.Serial(
port='/dev/serial0',
baudrate=9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
while 1:
   id = ser.readline()
   if len(id) != 0:
       print(id)
