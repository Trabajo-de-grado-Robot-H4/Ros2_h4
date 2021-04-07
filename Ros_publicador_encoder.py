#!/usr/bin/env python
# license removed for brevity

""" LIBRERÍAS """

import rclpy
from rclpy.node import Node      # DATOS POINT
from nuevas_interfaces.msg import Sens
import RPi.GPIO as GPIO                    # COMUNICACIÓN GPIO
import time                                # TIEMPO

""" OBJETOS """

Enc=Point()                                # OBJETO POINT
rospy.init_node('talker1', anonymous=True) # OBJETO NODO

""" PINES ENCODER """

RoAPin = 21
RoBPin = 20

""" VARIABLES """

gain=360/(11*34)
grados=0
count=0

""" SETUP """

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RoAPin, GPIO.IN)
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.add_event_detect(RoAPin, GPIO.FALLING, callback=callbackEncoder)

""" INTERRUPCIÓN ENCODERS """

def callbackEncoder(RoAPin):
     global gain
     global grados
     global count

     B= GPIO.input(RoBPin)
     if (B==1):
        count=count+1
     if (B==0):
        count=count-1
     grados=count*gain

""" LIMPIEZA PINES """

def destroy():
        GPIO.cleanup()

""" PUBLICADOR """

def talker():
    pub = rospy.Publisher('Encoder1', Point, queue_size=1000)
    rate = rospy.Rate(50)                                     # 50hz
    while not rospy.is_shutdown():
        Enc.x=grados
        pub.publish(Enc)
        rate.sleep()

""" PRINCIPAL """

if __name__ == '__main__':
    setup()
    try:
        talker()
    except rospy.ROSInterruptException:
        destroy()
        pass
