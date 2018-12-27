#!/usr/bin/python
import MySQLdb
import time
import RPi.GPIO as GPIO
import datetime
import picamera


GPIO.setmode(GPIO.BCM)
PIR = 21
GPIO.setup(26, GPIO.OUT)                                              # servo
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(12, GPIO.OUT)                                              # Definition du port en sortie
GPIO.setup(16, GPIO.OUT)                                              # Definition du port en sortie
GPIO.setwarnings(False)                                               # Mettre sur OFF les alertes (qui $
                                                           #position du cadre au lancement du programme


def servo(angle, ajoutAngle):
    pwm=GPIO.PWM(26,100)
    pwm.start(5)
    angleChoisi = float(angle)/10 + ajoutAngle
    pwm.ChangeDutyCycle(angleChoisi)
    time.sleep(5)
# fin def servo
servo(5, 5)

def  statut():
        db = MySQLdb.connect(host="ADRESSE IP",    # your host, usually localhost
                             user="LOGIN",         # your username
                             passwd="MDP",  # your password
                             db="NOM-DB")        # name of the data base
        cur = db.cursor()
        cur.execute("SELECT * FROM survey order by id desc LIMIT 0, 1")
        for row in cur.fetchall():

                statut1 = row[1]
                if statut1 == "no":
#                       a = "non active"
                        servo(5, 5)
#                       print a
#                       return statut1
                elif statut1 == "oui" and GPIO.input(PIR):
#                       a = "activation"
                        servo(70, 5)
                        print("Mouvement ! ")
                        GPIO.output(12, True)
                        #debut APN
                        with picamera.PiCamera() as camera:
                                camera.resolution = (1024, 768)
                                camera.start_preview()
                                time.sleep(1) #prechauffage APN
                                i = 0
                                nbpic=3
                                while i < nbpic :
                                        date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                                        camera.capture("/home/pi/scripts/pics/image"+ date + ".jpg")
                                        time.sleep(1)
                                        i = i + 1
                        #fin camera
                        GPIO.output(12, False)
#                       return statut1
                else:
#                       a = "activation"
                        servo(70, 5)
#                       print a
#                       return statut1
        db.close()
# fin def statut


try:
        print(" (CTRL+C to exit)")
        #GPIO.output(16, True)
        # nbpic = input ("entrez le nombre de photo par detection :\n")
        print "Ready"

        while True:
                statut()
#               GPIO.output(16, True)
                time.sleep(3)
#               GPIO.output(16, False)

except KeyboardInterrupt:
        print("Quit")
        servo(5, 5)
        GPIO.cleanup()
