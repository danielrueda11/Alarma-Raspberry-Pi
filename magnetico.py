import pymysql
import time  
import RPi.GPIO as GPIO
import smtplib
import serial
import subprocess
GPIO.setwarnings(False)
port=serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1) #puerto habilitado para conexion serial

door_pin = 4
buzzer= 16
azul = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)
GPIO.setup(azul, GPIO.OUT)
GPIO.output(azul, GPIO.LOW)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
	if GPIO.input(door_pin):     						#activacion del sensor de puerta magnetico
		with open("/home/pi/armado.txt", "r") as fo: 			#mismo proceso anterior de revision del archivo armado.txt
                        fo.seek(0, 0)
                        status = fo.read(1)
		fo.closed 
		print("PUERTA ABIERTA!")
		db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma") #conexion a base datos 
		cur=db.cursor()
		contador=cur.execute("select id from puerta")
		contador=contador+1
		print(contador)
		date=time.strftime('%Y- %m- %d %H: %M: %S')
		cur.execute("INSERT INTO puerta VALUES(%s,%s,%s)", (contador,date,"Puerta Abierta")) #registro de base de datos del sensor de la puerta
		db.commit()
		db.close()
		time.sleep(20)
		
		if (status == "1"):
			time.sleep(15)
			with open("/home/pi/armado.txt", "r") as fo:    #mismo proceso anterio de revision de archito armado.txt y activacion del proceso de alerta
				fo.seek(0, 0)
				status = fo.read(1)
			fo.closed 
			if (status == "1"):
				print("Clave Incorrecta")
				print("Intruso Detectado")
				GPIO.output(azul, GPIO.HIGH)
				GPIO.output(9, GPIO.LOW)
				GPIO.output(buzzer, GPIO.HIGH)
				time.sleep(5)
				GPIO.output(buzzer, GPIO.LOW)
				port.write('ATD04241613934;'+'\r\n')
				rcv = port.read(15)
				print (rcv)
				time.sleep(0.1)
				
				port.write('AT+CMGF=1'+'\r\n') 			
				rcv = port.read(15)
				print (rcv)

				port.write('AT+CNMI=2,1,0,0,0'+'\r\n') 			
				rcv = port.read(15)
				print (rcv)

				port.write('AT+CMGS="+584241613934"'+'\r\n') 			
				rcv = port.read(15)
				print (rcv)
					
				port.write('!!!!ALARMA ACTIVADA!!!!'+'\r\n') 			
				rcv = port.read(15)
				print (rcv)
					
				port.write("\x1A")
				for i in range(15):
					rcv=port.read(15)
					print (rcv)
			      
				FROM = "alarmaraspberry422@gmail.com"
				TO = ['danrueda11@gmail.com']
				TOstr = 'alarmaraspberry422@gmail.com'
				server = smtplib.SMTP('smtp.gmail.com',587)
				server.ehlo()
				server.starttls()
				server.ehlo
				server.login(FROM,'1234qazx')
				header = 'To:' + TOstr + '\n' + 'From: ' + FROM + '\n' + 'Subject:ALARMA ACTIVADA!!! \n'
				print (header)
				msg = header + '\n ALERTA!!!!\n ALARMA ACTIVADA, CONTACTE AL PERSONAL DE SEGURIDAD Y A LA POLICIA.\n CONTROLCA S.A\n'
				server.sendmail(FROM,TO,msg)
				print ("Listo !")
				server.quit()
				db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma")
				cur=db.cursor()
				contador=cur.execute("select id from puerta")
				contador=contador+1
				print(contador)
				date=time.strftime('%Y- %m- %d %H: %M: %S')
				cur.execute("INSERT INTO puerta VALUES(%s,%s,%s)", (contador,date,"Intruso Detectado"))
				db.commit()
				db.close()
				time.sleep(15)
GPIO.cleanup() #limpieza de GPIOs utilizados
