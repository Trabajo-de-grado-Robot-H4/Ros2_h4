#!/usr/bin/env python
# license removed for brevity

""" LIBRERÍAS """

import rclpy
from rclpy.node import Node      # DATOS POINT
from nuevas_interfaces.msg import Sens
import RPi.GPIO as GPIO                    # COMUNICACIÓN GPIO
import time                                # TIEMPO

""" PINES ENCODER """

RoAPin = 21
RoBPin = 20

""" VARIABLES """

gain=360/(11*34)
grados=0.0
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
     print ('Entré',grados)

""" LIMPIEZA PINES """

def destroy():
        GPIO.cleanup()

""" PUBLICADOR """
class MinimalPublisher(Node):

    def __init__(self,grados):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Sens, 'topic1', 10)     # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.grados=grados
        

    def timer_callback(self):
        
        msg = Sens()                                           # CHANGE
        msg.sens1 = self.grados                                      # CHANGE
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.sens1)  # CHANGE

def main(args=None):
    setup()
    global grados 
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(grados)

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()
""" PRINCIPAL """

if __name__ == '__main__':
    
    try:
        main()
    except rospy.ROSInterruptException:
        destroy()
        pass
