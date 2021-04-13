import rclpy
from rclpy.node import Node
#from nuevas_interfaces.msg import Sens
from geometry_msgs.msg import Point

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
    #asignamos la frecuencia del PWM
pca.frequency = 60

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(Point,'topic',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self,Point):
        #Pwm=Sens.sens1
        Pwm=Point.x
        self.get_logger().info('I heard: "%s"' % Pwm)

        if variable>=0:
            pca.channels[0].duty_cycle = abs(int(Pwm))
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 30000

        if variable_x<0:
            pca.channels[0].duty_cycle = abs(int(Pwm))
            pca.channels[1].duty_cycle = 30000
            pca.channels[2].duty_cycle = 0


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
