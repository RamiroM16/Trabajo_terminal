#include <controller_interface/controller_interface.hpp>
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>
#include <rclcpp/rclcpp.hpp>
#include <Eigen/Dense>
#include <realtime_tools/realtime_buffer.h>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <ament_index_cpp/get_package_share_directory.hpp>

// ONNX Runtime (El motor de IA)
#include <onnxruntime_cxx_api.h>

// Tus archivos de ayuda
#include "ur3_custom_control/ur3e_dynamics.hpp"
#include "ur3_custom_control/neural_parameters.hpp" // Escaladores generados por Python

namespace ur3_control_cpp
{

class NeuralTorqueController : public controller_interface::ControllerInterface
{
public:
    NeuralTorqueController() = default;

    controller_interface::CallbackReturn on_init() override
    {
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::CallbackReturn on_configure(
        const rclcpp_lifecycle::State & /*previous_state*/) override
    {
        joint_names_ = {"shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
                        "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"};

        // --- 1. CARGAR EL CEREBRO (ONNX) ---
        try {
            // Buscamos la ruta donde CMake instaló la carpeta 'config'
            std::string pkg_share = ament_index_cpp::get_package_share_directory("ur3_custom_control");
            std::string model_path = pkg_share + "/config/ur3_neural_controller.onnx";
            
            // Configurar Sesión ONNX para TIEMPO REAL
            // Es CRÍTICO usar 1 solo hilo para evitar latencia variable
            Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "UR3eNeural");
            Ort::SessionOptions session_options;
            session_options.SetIntraOpNumThreads(1); 
            session_options.SetInterOpNumThreads(1);
            
            // Cargar modelo a memoria RAM
            ort_session_ = std::make_unique<Ort::Session>(env, model_path.c_str(), session_options);
            
            RCLCPP_INFO(get_node()->get_logger(), "✅ CEREBRO ARTIFICIAL CARGADO: %s", model_path.c_str());

        } catch (const std::exception& e) {
            RCLCPP_ERROR(get_node()->get_logger(), "❌ ERROR FATAL CARGANDO ONNX: %s", e.what());
            return controller_interface::CallbackReturn::ERROR;
        }

        // Suscriptor de comandos (Trayectoria deseada)
        command_subscriber_ = get_node()->create_subscription<std_msgs::msg::Float64MultiArray>(
            "~/command", rclcpp::SystemDefaultsQoS(),
            [this](const std_msgs::msg::Float64MultiArray::SharedPtr msg) {
                if (msg->data.size() == 18) command_buffer_.writeFromNonRT(msg->data);
            });

        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::InterfaceConfiguration command_interface_configuration() const override
    {
        controller_interface::InterfaceConfiguration config;
        config.type = controller_interface::interface_configuration_type::INDIVIDUAL;
        for (const auto & joint : joint_names_) config.names.push_back(joint + "/" + hardware_interface::HW_IF_EFFORT);
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

    controller_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State &) override
    {
        // Posición segura inicial (Vertical "Cobra") para que no inicie con ceros
        std::vector<double> init_cmd(18, 0.0);
        init_cmd[1] = -1.57; init_cmd[3] = -1.57; 
        command_buffer_.initRT(init_cmd);
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State &) override
    {
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::return_type update(
        const rclcpp::Time &, const rclcpp::Duration &) override
    {
        // --- 2. LEER SENSORES (Estado Real) ---
        Eigen::VectorXd q(6), dq(6);
        for (size_t i = 0; i < 6; ++i) {
            q(i) = state_interfaces_[2 * i].get_value();
            dq(i) = state_interfaces_[2 * i + 1].get_value();
        }

        // --- 3. LEER COMANDO (Estado Deseado) ---
        std::vector<double> cmd = *command_buffer_.readFromRT();
        Eigen::VectorXd q_des(6), dq_des(6), ddq_des(6);
        for(int i=0; i<6; ++i) {
            q_des(i) = cmd[i]; dq_des(i) = cmd[i+6]; ddq_des(i) = cmd[i+12];
        }

        // --- 4. CÁLCULO FÍSICO (RNEA) ---
        // Usamos la física clásica como "pista" para la red
        Eigen::VectorXd tau_rnea = dynamics_solver_.rnea(q, dq, ddq_des);

        // --- 5. PREPARAR ENTRADA PARA LA RED (42 Valores) ---
        std::vector<float> input_tensor_values(42);
        int idx = 0;
        
        // Orden exacto del entrenamiento: q_act, dq_act, ddq_act, q_des, dq_des, ddq_des, tau_rnea
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)q(i);
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)dq(i);
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = 0.0f; // Aceleración actual ruidosa, usamos 0 como base
        
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)q_des(i);
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)dq_des(i);
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)ddq_des(i);
        
        for(int i=0; i<6; ++i) input_tensor_values[idx++] = (float)tau_rnea(i);

        // --- 6. NORMALIZACIÓN (Usando neural_parameters.hpp) ---
        // (x - mean) / scale
        for(size_t i=0; i<42; ++i) {
            input_tensor_values[i] = (input_tensor_values[i] - ur3_neural::input_mean[i]) / ur3_neural::input_scale[i];
        }
        

        // --- 7. INFERENCIA (Ejecutar ONNX) ---
        std::vector<int64_t> input_shape = {1, 42}; // Batch size 1, 42 features
        
        // Crear tensor de entrada
        Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
            memory_info, input_tensor_values.data(), input_tensor_values.size(), input_shape.data(), input_shape.size());

        const char* input_names[] = {"input"}; 
        const char* output_names[] = {"output"};

        // ⏱️ INICIO DEL CRONÓMETRO
        auto start = std::chrono::high_resolution_clock::now();

        // ¡Correr la red!
        auto output_tensors = ort_session_->Run(
            Ort::RunOptions{nullptr}, input_names, &input_tensor, 1, output_names, 1);
        
        // ⏱️ FIN DEL CRONÓMETRO
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Obtener puntero a los datos de salida
        float* floatarr = output_tensors.front().GetTensorMutableData<float>();
        
        // --- 8. POST-PROCESAMIENTO ---
        Eigen::VectorXd tau_cmd(6);
        for(int i=0; i<6; ++i) {
            // Des-normalizar: (y * scale) + mean
            double neural_out = (floatarr[i] * ur3_neural::output_scale[i]) + ur3_neural::output_mean[i];
            
            // Saturación de seguridad (Max 55 Nm para UR3e)
            // Esto evita que el robot "explote" si la red alucina
            if(neural_out > 55.0) neural_out = 55.0;
            if(neural_out < -55.0) neural_out = -55.0;
            
            tau_cmd(i) = neural_out;
        }

        // --- 9. ENVIAR A LOS MOTORES ---
        for (size_t i = 0; i < 6; ++i) {
            command_interfaces_[i].set_value(tau_cmd(i));
        }

        static int nn_report_cnt = 0;
if (nn_report_cnt++ % 100 == 0) {
    double total_sq_err = 0;
    for(int i=0; i<6; ++i) {
        double e = q_des(i) - q(i);
        total_sq_err += std::pow(e, 2);
    }
    double current_rmse = std::sqrt(total_sq_err / 6.0);

    // Identificador visual diferente para no confundirlo con el PD
    RCLCPP_INFO(get_node()->get_logger(), 
                "🧠 [NEURAL CONTROL] Inf: %ld us | RMSE: %.6f rad", 
                duration, current_rmse);
}

        return controller_interface::return_type::OK;
    }

private:
    std::vector<std::string> joint_names_;
    UR3eDynamics dynamics_solver_; 
    std::unique_ptr<Ort::Session> ort_session_; // Sesión persistente de ONNX
    
    realtime_tools::RealtimeBuffer<std::vector<double>> command_buffer_;
    rclcpp::Subscription<std_msgs::msg::Float64MultiArray>::SharedPtr command_subscriber_;
};

} // namespace

// Exportar Plugin
PLUGINLIB_EXPORT_CLASS(ur3_control_cpp::NeuralTorqueController, controller_interface::ControllerInterface)