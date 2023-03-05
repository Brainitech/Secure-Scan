#import libraries

import mysql.connector
import serial
from datetime import datetime

#connect to sql
try:
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="<database name>"  
  )
except Exception:
  print ("Sorry, something went wrong. Please try again")
  
#get date

tyd = datetime.now()
date = tyd.strftime("%B_%d_%Y")

#create log table

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS "+ date +" (RFID VARCHAR(15) NOT NULL, Time_In VARCHAR(8), Time_Out VARCHAR(8), FOREIGN KEY(RFID) REFERENCES Info(RFID)" )
mydb.commit()


mode = input("Add students-A   Scan Students-S:")

#Add student

if mode == 'A':
	Name= input("Type Student Name [Full Name] :")
	ID= input("Type Student ID number [2xM010xxx]:")
	Class= input("Type Student Class [01-12] :")
	Section= input("Type Student Section [A-Z] :")
	print ("Scan Your ID Card")
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
               break

#insert values into table

	mycursor = mydb.cursor()
	sql = "INSERT INTO Info (Studname, StudID, StudClass, StudSection, RFID) Values (%s, %s, %s, %s, %s)"
	val = (Name, ID, Class, Section, id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")

#Submission

elif mode == 'S':
     type = input("SUBMISSION-S   COLLECTION-C:")

     if type == 'S':
           for i in range(1):
              print ("Scan Your ID Card")
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
                     break

              mycursor = mydb.cursor(buffered=True)
              mycursor.execute("SELECT StudName, StudID, StudClass, StudSection FROM Info WHERE RFID=\""+id.decode('utf-8')+"\"")


              info = mycursor.fetchall()

              for inf in info:

                   print(inf)
              if info:
                pass
              else:
                print("Student Not Found")
              mycursor = mydb.cursor(buffered=True)
              mycursor.execute("UPDATE Info SET StudStatus = 1 WHERE RFID=\""+id.decode('utf-8')+"\"")
              mydb.commit()

              curr = datetime.now()
              time = curr.strftime("%H:%M:%S")
              mycursor = mydb.cursor(buffered=True)
              query = "UPDATE Info Set Time_In = %s WHERE  RFID=\""+id.decode('utf-8')+"\""
              tm = [curr.strftime("%H:%M:%S")]
              mycursor.execute(query, tm)
              mydb.commit()
              print("Student Checked In at", time)

#recording logs

              mycursor = mydb.cursor(buffered=True)
              query = "INSERT INTO {} (RFID, Time_In) VALUES(%s, %s)".format(date)
              mycursor.execute(query, (id, time))
              mydb.commit()

#collection

     if type == 'C':
           for i in range(1):
              print ("Scan Your ID Card")
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
                     break

              mycursor = mydb.cursor(buffered=True)
              mycursor.execute("SELECT StudName, StudID, StudClass, StudSection FROM Info WHERE RFID=\""+id.decode('utf-8')+"\"")


              info = mycursor.fetchall()

              for inf in info:

                  print(inf)
              if info:
                pass
              else:
                print("Student Not Found")

              mycursor = mydb.cursor(buffered=True)
              mycursor.execute("SELECT StudStatus FROM Info WHERE RFID=\""+id.decode('utf-8')+"\"")
              check = mycursor.fetchone()

              for chk in check:

                 if chk == (1):
                    mycursor = mydb.cursor(buffered=True)
                    mycursor.execute("UPDATE Info SET StudStatus = 0 WHERE RFID=\""+id.decode('utf-8')+"\"")
                    mydb.commit()
                    curr = datetime.now()
                    time = curr.strftime("%H:%M:%S")
                    mycursor = mydb.cursor(buffered=True)
                    query = "UPDATE Info Set Time_Out = %s WHERE  RFID=\""+id.decode('utf-8')+"\""
                    tm = [curr.strftime("%H:%M:%S")]
                    mycursor.execute(query, tm)
                    mydb.commit()

                    print("Student Checked Out at", time)
                 else:
                    print("Student Did Not Submit Any Device")


