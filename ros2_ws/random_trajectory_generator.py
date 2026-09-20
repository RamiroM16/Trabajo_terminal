import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import numpy as np
import time
import random

def quintic_polynomial(start_pos, end_pos, time_total, t):
    # Genera una curva suave s(t) de 0 a 1
    # p(t) = a0 + a1*t + a2*t^2 + a3*t^3 + a4*t^4 + a5*t^5
    # Condiciones: vel y acc inicial y final son 0.
    
    t = t / time_total # Normalizar tiempo 0 a 1
    s = 10*(t**3) - 15*(t**4) + 6*(t**5)
    ds = (30*(t**2) - 60*(t**3) + 30*(t**4)) / time_total
    dds = (60*t - 180*(t**2) + 120*(t**3)) / (time_total**2)
    
    pos = start_pos + (end_pos - start_pos) * s
    vel = (end_pos - start_pos) * ds
    acc = (end_pos - start_pos) * dds
    
    return pos, vel, acc

class RandomTrajectoryNode(Node):
    def __init__(self):
        super().__init__('random_trajectory_generator')
        self.pub = self.create_publisher(Float64MultiArray, '/custom_torque_controller/command', 10)
        self.timer = self.create_timer(0.01, self.control_loop) # 100 Hz

        # Límites del UR3e (aprox)
        self.joint_limits = np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]) 
        # Mantén rangos seguros para no golpear el suelo o auto-colisión
        self.q_min = np.array([-3.14, -2.5, -2.0, -3.0, -3.0, -3.0])
        self.q_max = np.array([ 3.14,  -0.6,  2.0,  3.0,  3.0,  3.0])

        self.current_q = np.array([0.0, -1.57, 0.0, -1.57, 0.0, 0.0]) # Inicio
        self.target_q = self.get_random_target()
        
        self.move_duration = 4.0 # Segundos por movimiento
        self.start_time = time.time()
        self.is_moving = True

        self.get_logger().info("Generador Aleatorio Iniciado. ¡Cuidado con el robot!")

    def get_random_target(self):
        return np.random.uniform(self.q_min, self.q_max)

    def control_loop(self):
        now = time.time()
        elapsed = now - self.start_time

        if elapsed > self.move_duration:
            # Llegamos al destino, generar uno nuevo
            self.current_q = self.target_q
            self.target_q = self.get_random_target()
            self.start_time = time.time()
            elapsed = 0
            # Variar la velocidad aleatoriamente también
            self.move_duration = random.uniform(2.0, 5.0) 

        # Calcular Spline para cada articulación
        q_cmd = []
        dq_cmd = []
        ddq_cmd = []

        for i in range(6):
            p, v, a = quintic_polynomial(self.current_q[i], self.target_q[i], self.move_duration, elapsed)
            q_cmd.append(p)
            dq_cmd.append(v)
            ddq_cmd.append(a)

        # Enviar comando
        msg = Float64MultiArray()
        msg.data = q_cmd + dq_cmd + ddq_cmd
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RandomTrajectoryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()