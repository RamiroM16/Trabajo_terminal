#include <controller_interface/controller_interface.hpp>
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>
#include <rclcpp/rclcpp.hpp>
#include <Eigen/Dense>
#include <realtime_tools/realtime_buffer.h>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <cmath>
#include <chrono>
#include <vector>

#include "ur3_custom_control/ur3e_dynamics.hpp"

namespace ur3_control_cpp
{

class ComputedTorqueController : public controller_interface::ControllerInterface
{
public:
    ComputedTorqueController() = default;

    controller_interface::CallbackReturn on_init() override
    {
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::CallbackReturn on_configure(
        const rclcpp_lifecycle::State & /*previous_state*/) override
    {
        joint_names_ = {"shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
                        "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"};

        // 1. Suscriptor de Comandos (Trayectoria desde Python)
        command_subscriber_ = get_node()->create_subscription<std_msgs::msg::Float64MultiArray>(
            "~/command", rclcpp::SystemDefaultsQoS(),
            [this](const std_msgs::msg::Float64MultiArray::SharedPtr msg) {
                if (msg->data.size() == 18) {
                    command_buffer_.writeFromNonRT(msg->data);
                }
            });

        // 2. Publicador de Datos de Entrenamiento (Para la Red Neuronal)
        data_publisher_ = get_node()->create_publisher<std_msgs::msg::Float64MultiArray>(
            "~/training_data", 10);

        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::InterfaceConfiguration command_interface_configuration() const override
    {
        controller_interface::InterfaceConfiguration config;
        config.type = controller_interface::interface_configuration_type::INDIVIDUAL;
        for (const auto & joint : joint_names_) {
            config.names.push_back(joint + "/" + hardware_interface::HW_IF_EFFORT);
        }
        return config;
    }

    controller_interface::InterfaceConfiguration state_interface_configuration() const override
    {
        controller_interface::InterfaceConfiguration config;
        config.type = controller_interface::interface_configuration_type::INDIVIDUAL;
        for (const auto & joint : joint_names_) {
            config.names.push_back(joint + "/" + hardware_interface::HW_IF_POSITION);
            config.names.push_back(joint + "/" + hardware_interface::HW_IF_VELOCITY);
        }
        return config;
    }

    controller_interface::CallbackReturn on_activate(
        const rclcpp_lifecycle::State & /*previous_state*/) override
    {
        // Inicializar buffer con posición segura (Vertical)
        std::vector<double> init_cmd(18, 0.0);
        init_cmd[1] = -1.57; // Hombro
        init_cmd[3] = -1.57; // Muñeca 1
        command_buffer_.initRT(init_cmd);
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::CallbackReturn on_deactivate(
        const rclcpp_lifecycle::State & /*previous_state*/) override
    {
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::return_type update(
        const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/) override
    {
        // 1. LEER ESTADO ACTUAL
        Eigen::VectorXd q(6), dq(6);
        for (size_t i = 0; i < 6; ++i) {
            q(i) = state_interfaces_[2 * i].get_value();
            dq(i) = state_interfaces_[2 * i + 1].get_value();
        }

        // 2. LEER COMANDO DEL BUFFER (Trayectoria deseada)
        std::vector<double> cmd = *command_buffer_.readFromRT();
        
        Eigen::VectorXd q_des(6), dq_des(6), ddq_des(6);
        for(int i=0; i<6; ++i) {
            q_des(i)   = cmd[i];
            dq_des(i)  = cmd[i + 6];
            ddq_des(i) = cmd[i + 12];
        }

        // ⏱️ INICIO DEL CRONÓMETRO
        auto start = std::chrono::high_resolution_clock::now();

        // 3. CALCULAR ERROR
        Eigen::VectorXd e = q_des - q;
        Eigen::VectorXd de = dq_des - dq;

        // 4. GANANCIAS PID
        Eigen::VectorXd Kp(6), Kd(6);
        Kp << 100.0, 100.0, 100.0, 30.0, 30.0, 10.0; 
        Kd << 10.0,  10.0,  10.0,  2.0,  2.0,  0.5;

        // 5. CALCULAR TORQUE (RNEA + PID)
        Eigen::VectorXd tau_rnea = dynamics_solver_.rnea(q, dq, ddq_des);
        Eigen::VectorXd tau_cmd(6);
        
        for(int i=0; i<6; ++i) {
            // Nota: RNEA da negativo para sostener, Motor necesita negativo. Se suman.
            tau_cmd(i) = tau_rnea(i) + (Kp(i) * e(i)) + (Kd(i) * de(i));
        }

        // ⏱️ FIN DEL CRONÓMETRO
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        static int report_count = 0;
        // Reportar cada 1 segundo (si el controlador corre a 100Hz)
        if (report_count++ % 100 == 0) {
            double sum_sq_error = 0.0;
            
            for (int i = 0; i < 6; ++i) {
                // Error de posición actual por articulación
                double error = q_des(i) - q(i);
                sum_sq_error += std::pow(error, 2);
            }

            // Cálculo del RMSE Global (Root Mean Square Error)
            double rmse = std::sqrt(sum_sq_error / 6.0);

            RCLCPP_INFO(get_node()->get_logger(), 
                "📊 [PD CLASSIC] Time: %ld us | RMSE: %.6f rad", 
                duration, rmse);
        }

        // 6. ENVIAR A MOTORES
        for (size_t i = 0; i < 6; ++i) {
            command_interfaces_[i].set_value(tau_cmd(i));
        }

        // --- A. PUBLICACIÓN DE DATOS (Para Red Neuronal y chequeo de Hz) ---
        // Usamos un nombre distinto: 'log_counter'
        static int log_counter = 0;
        if (log_counter++ % 5 == 0) { // Publicar cada 5 ciclos (aprox 100 Hz si base es 500Hz)
            std_msgs::msg::Float64MultiArray msg;
            // Estructura: 42 valores
            for(int k=0; k<6; k++) msg.data.push_back(q(k));       // q_act
            for(int k=0; k<6; k++) msg.data.push_back(dq(k));      // dq_act
            for(int k=0; k<6; k++) msg.data.push_back(q_des(k));   // q_des
            for(int k=0; k<6; k++) msg.data.push_back(dq_des(k));  // dq_des
            for(int k=0; k<6; k++) msg.data.push_back(ddq_des(k)); // ddq_des
            for(int k=0; k<6; k++) msg.data.push_back(tau_rnea(k));// tau_model
            for(int k=0; k<6; k++) msg.data.push_back(tau_cmd(k)); // tau_total
            
            data_publisher_->publish(msg);
        }

        // --- B. IMPRESIÓN EN TERMINAL (Opcional, para debug visual) ---
        // Usamos OTRO nombre distinto: 'print_counter'
        static int print_counter = 0;
        if (print_counter++ % 1000 == 0) {
             RCLCPP_INFO(get_node()->get_logger(), 
                "J1 Pos: %.2f | Des: %.2f | RNEA: %.2f | CMD: %.2f", 
                q(1), q_des(1), tau_rnea(1), tau_cmd(1));
        }

        return controller_interface::return_type::OK;
    }

private:
    std::vector<std::string> joint_names_;
    UR3eDynamics dynamics_solver_; 
    
    realtime_tools::RealtimeBuffer<std::vector<double>> command_buffer_;
    rclcpp::Subscription<std_msgs::msg::Float64MultiArray>::SharedPtr command_subscriber_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr data_publisher_;
};

} // namespace ur3_control_cpp

PLUGINLIB_EXPORT_CLASS(
    ur3_control_cpp::ComputedTorqueController,
    controller_interface::ControllerInterface)