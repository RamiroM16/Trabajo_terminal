#ifndef UR3E_DYNAMICS_HPP
#define UR3E_DYNAMICS_HPP

#include <Eigen/Dense>
#include <vector>
#include <cmath>
#include <iostream>

class UR3eDynamics {
public:
    // Constructor: Inicializa parámetros físicos y DH
    UR3eDynamics() {
        // 1. Parámetros DH Modificados (Validados en MATLAB)
        // Orden: [alpha(i-1), a(i-1), d(i), theta_offset]
        dh_params.resize(6);
        dh_params[0] << 0.0,        0.0,       0.15185, 0.0;
        dh_params[1] << M_PI/2.0,   0.0,       0.0,     0.0;
        dh_params[2] << 0.0,       -0.24355,   0.0,     0.0;
        dh_params[3] << 0.0,       -0.2132,    0.13105, 0.0;
        dh_params[4] << M_PI/2.0,   0.0,       0.08535, 0.0;
        dh_params[5] << -M_PI/2.0,  0.0,       0.0921,  0.0;

        // 2. Masas (kg)
        mass = {2.0, 3.44, 1.44, 0.87, 0.80, 0.26};

        // 3. Centros de Masa (CoM) locales
        // IMPORTANTE: Pon aquí los valores exactos si los cambiaste en MATLAB
        com.resize(6);
        com[0] << 0.0, 0.0, -0.02;
        com[1] << -0.11355, 0.0, 0.1157;
        com[2] << -0.1632, 0.0, 0.0238;
        com[3] << 0.0, -0.01, 0.0;
        com[4] << 0.0, 0.01, 0.0;
        com[5] << 0.0, 0.0, -0.02;

        // 4. Tensores de Inercia (Aprox diagonales)
        inertia.resize(6);
        for(int i=0; i<6; ++i) {
            inertia[i] = Eigen::Matrix3d::Identity() * 0.01; 
        }
        
        // Eje Z unitario para rotaciones
        z0 << 0, 0, 1;
        
        // Gravedad "hacia arriba" para el algoritmo RNEA (Base frame)
        gravity_vec << 0, 0, 9.81;
    }

    // FUNCIÓN PRINCIPAL RNEA (Real-time safe)
    Eigen::VectorXd rnea(const Eigen::VectorXd& q, 
                         const Eigen::VectorXd& dq, 
                         const Eigen::VectorXd& ddq) 
    {
        // Inicialización de vectores (N+1 para incluir la base en índice 0)
        // Usamos std::vector de Eigen types para manejo dinámico simple
        std::vector<Eigen::Vector3d> w(7, Eigen::Vector3d::Zero());
        std::vector<Eigen::Vector3d> dw(7, Eigen::Vector3d::Zero());
        std::vector<Eigen::Vector3d> dv(7, Eigen::Vector3d::Zero());
        
        // Almacenamiento para la vuelta
        std::vector<Eigen::Matrix3d> R_store(7);
        std::vector<Eigen::Vector3d> P_store(7);

        // CONDICIÓN INICIAL (BASE)
        // La base (índice 0) está quieta, pero aceleramos "arriba" para gravedad
        dv[0] = gravity_vec; 

        // --- 1. PASADA HACIA ADELANTE (Forward Pass) ---
        for (int i = 0; i < 6; ++i) {
            // Índices:
            // i   -> Joint actual (0 a 5 en C++ corresponde a 1 a 6 en teoría)
            // idx -> Índice en los arrays w, dw (idx=1 es Joint 1)
            int idx = i + 1;
            int prev = i;

            // Extraer DH
            double alpha = dh_params[i][0];
            double a     = dh_params[i][1];
            double d     = dh_params[i][2];
            double theta = q(i);

            double ct = std::cos(theta);
            double st = std::sin(theta);
            double ca = std::cos(alpha);
            double sa = std::sin(alpha);

            // Matriz de Rotación (i-1 a i)
            Eigen::Matrix3d R;
            R << ct,    -st,     0,
                 st*ca,  ct*ca, -sa,
                 st*sa,  ct*sa,  ca;
            
            // Transpuesta (R de i respecto a i-1)
            Eigen::Matrix3d Rt = R.transpose();
            R_store[idx] = R; // Guardamos la normal para la vuelta

            // Vector Posición P (i-1 a i)
            Eigen::Vector3d P;
            P << a, -d*sa, d*ca;
            P_store[idx] = P;

            // Propagación Cinemática
            Eigen::Vector3d z_axis = z0 * dq(i);       // q_dot * z0
            Eigen::Vector3d z_accel = z0 * ddq(i);     // q_ddot * z0

            // Velocidad Angular
            w[idx] = Rt * w[prev] + z_axis;

            // Aceleración Angular
            // dw = Rt*dw_prev + cross(Rt*w_prev, z_axis) + z_accel
            dw[idx] = Rt * dw[prev] + (Rt * w[prev]).cross(z_axis) + z_accel;

            // Aceleración Lineal
            // dv = Rt*dv_prev + cross(dw, P) + cross(w, cross(w, P))
            dv[idx] = Rt * dv[prev] + dw[idx].cross(P) + w[idx].cross(w[idx].cross(P));
        }

        // --- 2. PASADA HACIA ATRÁS (Backward Pass) ---
        Eigen::VectorXd tau = Eigen::VectorXd::Zero(6);
        std::vector<Eigen::Vector3d> f(7, Eigen::Vector3d::Zero());
        std::vector<Eigen::Vector3d> n(7, Eigen::Vector3d::Zero());

        for (int i = 5; i >= 0; --i) {
            int idx = i + 1; // Actual (1-based logic stored in vector)
            
            // Aceleración del Centro de Masa
            // dv_com = dv + cross(dw, com) + cross(w, cross(w, com))
            Eigen::Vector3d dv_com = dv[idx] + dw[idx].cross(com[i]) + 
                                     w[idx].cross(w[idx].cross(com[i]));

            // Fuerza Inercial (F = ma)
            Eigen::Vector3d F_inertial = mass[i] * dv_com;

            // Torque Inercial (N = I*dw + cross(w, I*w))
            Eigen::Vector3d N_inertial = inertia[i] * dw[idx] + 
                                         w[idx].cross(inertia[i] * w[idx]);

            // Balance de Fuerzas y Torques
            if (i == 5) {
                // Último eslabón (sin carga externa por ahora)
                f[idx] = F_inertial;
                n[idx] = N_inertial + com[i].cross(F_inertial);
            } else {
                // Eslabones intermedios
                // Recuperamos R y P del siguiente eslabón (i+1)
                // Ojo: R_store[idx+1] es la R de (i) a (i+1)
                Eigen::Matrix3d R_next = R_store[idx+1];
                Eigen::Vector3d P_next = P_store[idx+1];

                Eigen::Vector3d f_next_rot = R_next * f[idx+1];
                Eigen::Vector3d n_next_rot = R_next * n[idx+1];

                f[idx] = f_next_rot + F_inertial;
                
                n[idx] = n_next_rot + P_next.cross(f_next_rot) + 
                         N_inertial + com[i].cross(F_inertial);
            }

            // Proyección en eje Z (Torque del Motor)
            tau(i) = n[idx].dot(z0);
        }

        return tau;
    }

private:
    std::vector<Eigen::Vector4d> dh_params;
    std::vector<double> mass;
    std::vector<Eigen::Vector3d> com;
    std::vector<Eigen::Matrix3d> inertia;
    
    Eigen::Vector3d z0;
    Eigen::Vector3d gravity_vec;
};

#endif // UR3E_DYNAMICS_HPP