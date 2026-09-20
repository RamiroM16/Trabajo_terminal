import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import GetParameters
import xml.etree.ElementTree as ET

def main():
    rclpy.init()
    node = Node('param_inspector')

    # Conectar al robot_state_publisher para pedir el URDF real
    client = node.create_client(GetParameters, '/robot_state_publisher/get_parameters')
    while not client.wait_for_service(timeout_sec=1.0):
        print("Esperando servicio de robot_state_publisher...")

    req = GetParameters.Request()
    req.names = ['robot_description']

    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)

    try:
        xml_string = future.result().values[0].string_value
        root = ET.fromstring(xml_string)

        print(f"{'LINK':<15} | {'MASA (kg)':<10} | {'CoM (x, y, z)':<30}")
        print("-" * 60)

        # Recorrer links buscando datos inerciales
        target_links = ['shoulder_link', 'upper_arm_link', 'forearm_link', 
                        'wrist_1_link', 'wrist_2_link', 'wrist_3_link']

        for link in root.findall('link'):
            name = link.get('name')
            if any(t in name for t in target_links):
                inertial = link.find('inertial')
                if inertial is not None:
                    mass = inertial.find('mass').get('value')
                    origin = inertial.find('origin').get('xyz')
                    print(f"{name:<15} | {mass:<10} | {origin:<30}")

    except Exception as e:
        print(f"Error parseando URDF: {e}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
