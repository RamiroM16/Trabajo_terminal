
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time

class SineWaveGenerator(Node):
    def __init__(self):
        super().__init__('sine_wave_generator')
        
        # Publicador al tópico de tu controlador
        # Nota: El nombre puede variar según tu namespace. 
        # Si usas "ros2 node list", busca el nombre de tu controller.
        self.publisher_ = self.create_publisher(
            Float64MultiArray, 
            '/custom_torque_controller/command', 
            10)
        
        self.timer = self.create_timer(0.01, self.timer_callback) # 100 Hz
        self.start_time = time.time()
        self.get_logger().info("Generador de Trayectoria Iniciado...")

    def timer_callback(self):
        t = time.time() - self.start_time
        
        # Parámetros de la onda
        amp = 0.5   # Amplitud (radianes)
        freq = 1.0  # Frecuencia (rad/s)
        center = -1.57 # Centro (Vertical)

        # 1. Calcular Cinemática de la Trayectoria (Solo Hombro)
        pos = center + amp * math.sin(freq * t)
        vel = amp * freq * math.cos(freq * t)
        acc = -amp * (freq**2) * math.sin(freq * t)

        # 2. Empaquetar mensaje (18 valores)
        # [q1...q6, dq1...dq6, ddq1...ddq6]
        msg = Float64MultiArray()
        
        q_vec = [0.0, pos, 0.0, -1.57, 0.0, 0.0]
        dq_vec = [0.0, vel, 0.0, 0.0, 0.0, 0.0]
        ddq_vec = [0.0, acc, 0.0, 0.0, 0.0, 0.0]
        
        # Concatenar todo en una sola lista plana
        msg.data = q_vec + dq_vec + ddq_vec
        
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SineWaveGenerator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()