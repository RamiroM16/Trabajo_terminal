import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib 
import os

# --- 1. CARGAR DATOS ---
print("Cargando dataset...")
df = pd.read_csv('dataset_ur3_full.csv')

# Definir columnas (Asegúrate de que coincidan con tu CSV)
joints = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
input_cols = []
# Entradas (42 variables)
for j in joints: input_cols.append(f'q_act_{j}')
for j in joints: input_cols.append(f'dq_act_{j}')
for j in joints: input_cols.append(f'ddq_act_{j}') # Usamos la calculada/filtrada
for j in joints: input_cols.append(f'q_des_{j}')
for j in joints: input_cols.append(f'dq_des_{j}')
for j in joints: input_cols.append(f'ddq_des_{j}')
for j in joints: input_cols.append(f'tau_rnea_{j}')

# Salidas (6 variables)
output_cols = []
for j in joints: output_cols.append(f'tau_cmd_{j}')

X = df[input_cols].values
y = df[output_cols].values

# --- 2. CREAR Y GUARDAR ESCALADORES (AQUÍ ESTÁ LA CLAVE) ---
print("Normalizando datos...")

# Creamos los objetos matemáticos
scaler_X = StandardScaler()
scaler_y = StandardScaler()

# 1. Calculamos la media y desviación (fit) Y transformamos los datos (transform)
# Estos X_scaled y y_scaled son los que LA RED VA A VER.
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# 2. Guardamos la "calculadora" para el futuro
# Esto es vital para cuando queramos ejecutar la red en el robot real.
joblib.dump(scaler_X, 'scaler_X.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')
print("Escaladores guardados como .pkl (No los borres, los necesitas para el robot).")

# --- 3. PREPARAR ENTRENAMIENTO ---
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# --- 4. DEFINIR ARQUITECTURA DE LA RED ---
def build_model(input_dim, output_dim):
    model = Sequential()
    # Capa de entrada (42 neuronas) -> Capa oculta
    model.add(Dense(128, input_dim=input_dim, activation='relu'))
    
    # Capas profundas
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.1)) # Prevenir memorización
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    
    # Capa de salida (6 neuronas = 6 torques)
    # Activación lineal porque queremos valores continuos (negativos y positivos)
    model.add(Dense(output_dim, activation='linear'))
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

model = build_model(input_dim=42, output_dim=6)

# --- 5. ENTRENAR ---
print("Iniciando entrenamiento...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=50,          # Puedes subirlo a 100 o 200 si mejora
    batch_size=32,
    verbose=1
)

# --- 6. GUARDAR MODELO ---
model.save('ur3_neural_controller.keras')
print("Modelo guardado exitosamente.")

# --- 7. PRUEBA RÁPIDA (Validación visual) ---
print("\n--- PRUEBA DE PREDICCIÓN ---")
# Tomamos una muestra aleatoria del test
sample_idx = 0
sample_input = X_test[sample_idx].reshape(1, -1) # Vector fila
real_output_scaled = y_test[sample_idx]

# La red predice (en escala normalizada)
pred_scaled = model.predict(sample_input)

# Invertimos la escala para ver Newtons-Metro reales
pred_real = scaler_y.inverse_transform(pred_scaled)
truth_real = scaler_y.inverse_transform(real_output_scaled.reshape(1, -1))

print(f"Torque Predicho (J1): {pred_real[0][0]:.3f} Nm")
print(f"Torque Real (J1):     {truth_real[0][0]:.3f} Nm")
print(f"Diferencia:           {abs(pred_real[0][0] - truth_real[0][0]):.3f} Nm")