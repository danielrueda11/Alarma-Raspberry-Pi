import RPi.GPIO as GPIO
import time
import subprocess
import pymysql

GPIO.setwarnings(False)

buzzer=16
verde=10
rojo=9
azul=7
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)
GPIO.setup(verde, GPIO.OUT) #LEDverde
GPIO.output(verde, GPIO.HIGH)
GPIO.setup(rojo, GPIO.OUT) #LEDrojo
GPIO.output(rojo, GPIO.LOW)
GPIO.setup(azul, GPIO.OUT) #LEDazul
GPIO.output(azul, GPIO.LOW)
 
class keypad():
    # CONSTANTS   
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
     
    ROW         = [21,26,19,13]
    COLUMN      = [6,5,0]
     
    def getKey(self):
         
        
        # Establece todas las columnas como salidas, bajas
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Establece todas las filas como entrada
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Escanear filas para tecla / boton pulsado
        # Una pulsacion de tecla valida debe establecer "rowVal" entre 0 y 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # Si rowVal no es de 0 a 3, entonces no se presiono ningun boton y podemos salir
        if rowVal < 0 or rowVal > 3:
            self.exit()
            return
         
        # Convertir columnas a entrada
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Cambiar la fila i-esima encontrada de escaneo a salida
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Escanear columnas en busca de teclas / botones aun presionados
        # Una pulsacion de tecla valida debe establecer "colVal" entre 0 y 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # Si colVal no es de 0 a 2, entonces no se presiono ningun boton y podemos salir.
        if colVal < 0 or colVal > 2:
            self.exit()
            return
 
        # Devuelve el valor de la tecla presionada
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        #Reinicializar todas las filas y columnas como entrada al salir 
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    
    kp = keypad()   #llamamos a la clase creada para el keypad
    posicion = "0000" #posicion en la que se van a digitar los numeros
    acceso = "1234"   #clave de acceso 
    apagado = "4321" #clave de apagado del sistema
    with open("/home/pi/armado.txt", "r+") as fo: #abrimos el archivo armado.txt y escribimos 0
        fo.seek(0, 0)
        fo.write("0")
    fo.closed
    
    time.sleep(5)
    print("Sistema Listo")
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer, GPIO.LOW)
    

    #creamos el ciclo de armado y desarmado de la alarma
    while True:
        digito = None #creamos la variable digito, en ella guardamos el numero ingresado en el keypad
        while digito == None:
            digito = kp.getKey() #activamos el keypad para digitar y guardar la informacion 
     
        
        print (digito)
        posicion = (posicion[1:] + str(digito))  #la posicion del digito se va llenando desde la derecha a izquierda segun la posicion antes creada
        print (posicion)

        if (posicion == acceso): #posicion es igual a acceso cuando la clave ha sido digitada correctamente
            with open("/home/pi/armado.txt", "r+") as fo: #abrimos el archivo armado.txt para leer su contenido
                fo.seek(0, 0)
                status = fo.read(1) #si el archivo contiene un uno ingresamos a la siguiente condicion 
            fo.closed
            time.sleep(1)
            if (status == "1"):
                with open("/home/pi/armado.txt", "r+") as fo: #abrimos el archivo para digitar la clave y apagar la alarma escribiendo 0
                    fo.seek(0, 0)
                    fo.write("0")
                fo.closed
                GPIO.output(verde, GPIO.HIGH) #se activa el led verde
                GPIO.output(rojo, GPIO.LOW) 
                GPIO.output(azul, GPIO.LOW)
                print("Alarma Desarmada")
                db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma") #conectamos a la base de datos del keypad llamada teclado
                cur=db.cursor()
                contador=cur.execute("SELECT id FROM teclado")
                contador=contador+1
                print(contador)
                date=time.strftime('%Y- %m- %d %H: %M: %S')
                cur.execute("INSERT INTO teclado VALUES(%s,%s,%s)", (contador,date,"Alarma Desarmada"))
                db.commit()
                db.close()
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(buzzer, GPIO.LOW)
                time.sleep(9.5)
            else: #cuando la alarma esta desactivada y ingresamos la clave de acceso, entra en el else y se arma la alarma
                GPIO.output(verde, GPIO.LOW) 
                GPIO.output(rojo, GPIO.HIGH) #se activa el rojo 
                print("Alarma Armada")
                db = pymysql.connect(host="localhost",user="pi",passwd="controlca",database="alarma")
                cur=db.cursor()
                contador=cur.execute("SELECT id FROM teclado")
                contador=contador+1
                print(contador)
                date=time.strftime('%Y- %m- %d %H: %M: %S')
                cur.execute("INSERT INTO teclado VALUES(%s,%s,%s)", (contador,date,"Alarma Armada"))
                db.commit()
                db.close()
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(buzzer, GPIO.LOW)
                time.sleep(19.5)
                with open("/home/pi/armado.txt", "r+") as fo:# al armarse la alarma ingresamos en el archivo armado.txt
                    fo.seek(0, 0)
                    fo.write("1") #se escribe en este else en numero 1 en el archivo armado.txt, con esto los sensores al activarse y leer 1 notificaran de la intrusion 
                fo.closed
        elif (posicion == apagado): #cuando la posicion es igual a apagado, la alarma es apagada
            print("Apagar Alarma")
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(buzzer,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            time.sleep(0.5)
            subprocess.call("halt", shell=True)
        
        time.sleep(0.5)
GPIO.cleanup() #limpieza de GPIOs utilizados
