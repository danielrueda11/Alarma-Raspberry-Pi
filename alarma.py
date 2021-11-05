import pymysql
import time  
import RPi.GPIO as GPIO
import smtplib
import serial
import subprocess

GPIO.setwarnings(False)

proceso1 = subprocess.Popen(['python', 'keypad.py']) #Ejecutar proceso1(script de keypad en simultaneo)
proceso2 = subprocess.Popen(['python', 'sensormagnetico.py']) 
port=serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1) #puerto habilitado para conexion serial
port.write('AT;'+'\r\n') 			#puerto serial activado para llamar al numero receptor
rcv = port.read(15)
print (rcv)
port.write('AT+CREG?;'+'\r\n') 			#puerto serial activado para llamar al numero receptor
rcv = port.read(15)
print (rcv)
port.write('AT+CSTT="internet.movistar.ve";'+'\r\n') 			#puerto serial activado para llamar al numero receptor
rcv = port.read(15)
print (rcv)
time.sleep(1)
port.write('AT+CIICR;'+'\r\n') 			#puerto serial activado para llamar al numero receptor
rcv = port.read(15)
print (rcv)
time.sleep(1)
port.write('AT+CIFSR;'+'\r\n') 			#puerto serial activado para llamar al numero receptor
rcv = port.read(15)
print (rcv)
time.sleep(1)
			
#sensores y componente utilizados
pir_pin = 20
buzzer= 16
azul = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)
GPIO.setup(azul, GPIO.OUT)
GPIO.output(azul, GPIO.LOW)
GPIO.setup(9, GPIO.OUT)


previous_pir=0 				#posicion previa de los sensores infrarrojos

#comienzo del ciclo de ejecucion de lo sensores detectores
while True:
	current_pir=GPIO.input(pir_pin)
	if previous_pir==0 and current_pir==1: 		#deteccion, cambio de estado
		with open("/home/pi/armado.txt", "r") as fo:                           # abrimos el archivo txt para verificar el estado
                    fo.seek(0, 0)
                    status = fo.read(1)						       #leemos el archivo
		fo.closed
		print ("Movimiento Detectado" + str(status))
		db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma") 		#conexion a la base de datos
		cur=db.cursor()
		contador=cur.execute("select id from movimiento")				      		#creamos un contador para el incremento del id de la base de datos
		contador=contador+1
		print(contador)
		date=time.strftime('%Y- %m- %d %H: %M: %S')
		cur.execute("INSERT INTO movimiento VALUES(%s,%s,%s)", (contador,date,"Movimiento Detectado")) 		#se crea e registro en la base de datos
		db.commit()
		db.close()
		if (status == '1'):
			print("Intruso Detectado")
			GPIO.output(azul, GPIO.HIGH)
			GPIO.output(9, GPIO.LOW)
			GPIO.output(buzzer, GPIO.HIGH)
			time.sleep(5)
			GPIO.output(buzzer, GPIO.LOW)
			port.write('ATD04265190385;'+'\r\n') 	        #puerto serial activado para llamar al numero receptor
			rcv = port.read(15)
			print (rcv)
			time.sleep(0.1)

			port.write('AT+CMGF=1'+'\r\n') 			#puerto serial activado para enviar mensaje de texto gsm
			rcv = port.read(15)
			print (rcv)

			port.write('AT+CNMI=2,1,0,0,0'+'\r\n') 			#formato del mensaje 
			rcv = port.read(15)
			print (rcv)

			port.write('AT+CMGS="+04127096202"'+'\r\n') 			#numero receptor del mensaje de texto gsm
			rcv = port.read(15)
			print (rcv)
				
			port.write('!!!!ALARMA ACTIVADA!!!!'+'\r\n') 			#mensaje de texto
			rcv = port.read(15)
			print (rcv)
				
			port.write("\x1A")
			for i in range(15):
				rcv=port.read(15)
				print (rcv)
			
			port.write('AT+CMGF=1'+'\r\n') 			
			rcv = port.read(15)
			print (rcv)

			port.write('AT+CNMI=2,1,0,0,0'+'\r\n') 			#puerto serial activado para llamar al numero receptor
			rcv = port.read(15)
			print (rcv)

			port.write('AT+CMGS="+584241613934"'+'\r\n') 			#puerto serial activado para llamar al numero receptor
			rcv = port.read(15)
			print (rcv)
				
			port.write('!!!!ALARMA ACTIVADA!!!!'+'\r\n') 			
			rcv = port.read(15)
			print (rcv)
				
			port.write("\x1A")
			for i in range(15):
				rcv=port.read(15)
				print (rcv)

			FROM = "alarmaraspberry422@gmail.com"  			#datos de la cuenta de correo electronico emisora del mensaje
			TO = ['danrueda11@gmail.com','ma.izaramend@gmail.com','bcante@gmail.com']					#dato del correo receptor del mensaje
			TOstr = 'alarmaraspberry422@gmail.com'
			server = smtplib.SMTP('smtp.gmail.com',587) 		#servidor smpt asignado
			server.ehlo()
			server.starttls()
			server.ehlo
			server.login(FROM,'1234qazx')           #clave de acceso del correo emisor
			header = 'To:' + TOstr + '\n' + 'From: ' + FROM + '\n' + 'Subject:ALARMA ACTIVADA!!! \n' #comunicado del mensaje
			print (header)
			msg = header + '\n ALERTA !!!!\n\n\nALARMA ACTIVADA, CONTACTE AL PERSONAL DE SEGURIDAD Y A LA POLICIA.\n\n\nCONTROLCA S.A'
			server.sendmail(FROM,TO,msg)                        #servidor del emisor y receptor 
			print ("Listo !")
			server.quit()                                      #salir del servidor
			db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma")
			cur=db.cursor()
			contador=cur.execute("select id from movimiento")
			contador=contador+1
			print(contador)
			date=time.strftime('%Y- %m- %d %H: %M: %S')
			cur.execute("INSERT INTO movimiento VALUES(%s,%s,%s)", (contador,date,"Intruso Detectado")) 		#registra el acontecimiento 
			db.commit()
			db.close()
			time.sleep(15)
	
				
	previous_pir=current_pir 					#vuelve el sensor infrarrojo a su estado inicial 
	time.sleep(1)
GPIO.cleanup() #limpieza de GPIOs utilizados
