import joblib
import numpy as np
import os

# 1. Cargar los escaladores
print("Cargando escaladores...")
try:
    scaler_X = joblib.load('scaler_X.pkl')
    scaler_y = joblib.load('scaler_y.pkl')
except FileNotFoundError:
    print("Error: No encuentro los archivos .pkl en esta carpeta.")
    exit()

# 2. Extraer media y escala (desviación estándar)
mean_in = scaler_X.mean_
scale_in = scaler_X.scale_

mean_out = scaler_y.mean_
scale_out = scaler_y.scale_

# 3. Generar el archivo de cabecera C++
header_content = f"""#ifndef NEURAL_PARAMETERS_HPP
#define NEURAL_PARAMETERS_HPP

#include <vector>
#include <cmath>

namespace ur3_neural {{

// Constantes de Normalización (Generadas automáticamente por Python)
// Input Dim: {len(mean_in)} | Output Dim: {len(mean_out)}

const std::vector<double> input_mean = {{
    {', '.join(map(str, mean_in))}
}};

const std::vector<double> input_scale = {{
    {', '.join(map(str, scale_in))}
}};

const std::vector<double> output_mean = {{
    {', '.join(map(str, mean_out))}
}};

const std::vector<double> output_scale = {{
    {', '.join(map(str, scale_out))}
}};

}} // namespace ur3_neural

#endif // NEURAL_PARAMETERS_HPP
"""

# 4. Guardar
output_path = "src/ur3_custom_control/include/ur3_custom_control/neural_parameters.hpp"
# Asegurar que la carpeta existe (ajusta la ruta si tu src está en otro lado)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    f.write(header_content)

print(f"¡Éxito! Archivo C++ generado en: {output_path}")
print("Ahora tu controlador C++ ya conoce las matemáticas de normalización.")