import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
import onnx

# --- 1. PREPARACIÓN DE DATOS ---
print("--- CARGANDO DATASET ---")
filename = 'dataset_ur3_final_1.csv'

if not os.path.exists(filename):
    print(f"ERROR: No se encuentra {filename}")
    exit()

df = pd.read_csv(filename)

joints = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
input_cols = []

# Definimos las 42 Entradas
for j in joints: input_cols.append(f'q_act_{j}')
for j in joints: input_cols.append(f'dq_act_{j}')
for j in joints: input_cols.append(f'ddq_act_{j}') 
for j in joints: input_cols.append(f'q_des_{j}')
for j in joints: input_cols.append(f'dq_des_{j}')
for j in joints: input_cols.append(f'ddq_des_{j}')
for j in joints: input_cols.append(f'tau_rnea_{j}')

# Definimos las 6 Salidas
output_cols = []
for j in joints: output_cols.append(f'tau_cmd_{j}')

# Extraer valores
X = df[input_cols].values
y = df[output_cols].values

print(f"Dataset cargado: {len(df)} muestras.")

# --- 2. NORMALIZACIÓN ---
print("--- NORMALIZANDO DATOS ---")
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Guardar escaladores (VITAL para C++)
joblib.dump(scaler_X, 'scaler_X.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')
print("Escaladores guardados (.pkl).")

# Convertir a Tensores
X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
y_tensor = torch.tensor(y_scaled, dtype=torch.float32)

# --- 3. DATALOADERS ---
X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)

# Lotes de 64 para ir un poco más rápido y estable
BATCH_SIZE = 512
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# --- 4. ARQUITECTURA MEJORADA (UR3eNetwork Pro) ---
class UR3eNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(UR3eNetwork, self).__init__()
        # Red más ancha y profunda para capturar dinámicas complejas
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),  # Entrada más ancha
            nn.ReLU(),
            
            nn.Linear(256, 512),        # Capa potente
            nn.ReLU(),
            nn.Dropout(0.05),           # Dropout bajo (solo regularización leve)
            
            nn.Linear(512, 256),
            nn.ReLU(),
            
            nn.Linear(256, 128),
            nn.ReLU(),
            
            nn.Linear(128, output_dim)
        )

    def forward(self, x):
        return self.net(x)

# Configuración GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Entrenando en: {device}")

model = UR3eNetwork(input_dim=42, output_dim=6).to(device)

# --- 5. OPTIMIZACIÓN Y SCHEDULER ---
criterion = nn.MSELoss()
# Learning Rate inicial un poco más alto, el scheduler lo bajará
optimizer = optim.Adam(model.parameters(), lr=0.002) 

# Scheduler: Reduce el LR a la mitad (factor 0.5) si el Loss no mejora en 15 épocas
# NOTA: Quitamos 'verbose=True' para evitar el error de versión de PyTorch
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=15)

# --- 6. BUCLE DE ENTRENAMIENTO ---
print("--- INICIANDO ENTRENAMIENTO (500 Épocas) ---")
epochs = 500

for epoch in range(epochs):
    model.train()
    train_loss = 0.0
    
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
    
    avg_loss = train_loss / len(train_loader)
    
    # Paso del Scheduler
    scheduler.step(avg_loss)
    
    # Monitoreo
    if (epoch+1) % 10 == 0:
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Epoch {epoch+1}/{epochs} | Loss (MSE): {avg_loss:.6f} | LR: {current_lr:.6f}")

# --- 7. GUARDAR Y EXPORTAR ---
print("--- GUARDANDO MODELO ---")
# 1. PyTorch Nativo
torch.save(model.state_dict(), 'ur3_neural_controller.pth')

# 2. ONNX (Para C++)
dummy_input = torch.randn(1, 42).to(device)
torch.onnx.export(model,
                  dummy_input,
                  "ur3_neural_controller.onnx",
                  export_params=True,
                  opset_version=9,    # Versión estable
                  do_constant_folding=True,
                  input_names = ['input'],
                  output_names = ['output'],
                  dynamic_axes={'input' : {0 : 'batch_size'},
                                'output' : {0 : 'batch_size'}})


onnx_model = onnx.load("ur3_neural_controller.onnx")
onnx_model.ir_version = 9
onnx.save(onnx_model, "ur3_neural_controller.onnx")

print("Modelo exportado a ONNX exitosamente.")

# --- 8. PRUEBA DE PRECISIÓN ---
model.eval()
with torch.no_grad():
    # Tomar primera muestra del test set
    sample_input = X_test[0].unsqueeze(0).to(device)
    target_output = y_test[0].unsqueeze(0).cpu().numpy()
    
    pred_scaled = model(sample_input).cpu().numpy()
    
    # Invertir escala
    pred_real = scaler_y.inverse_transform(pred_scaled)
    target_real = scaler_y.inverse_transform(target_output)
    
    diff = abs(pred_real[0][0] - target_real[0][0])
    
    print("\n--- RESULTADO FINAL (Joint 1 - Hombro) ---")
    print(f"Predicho: {pred_real[0][0]:.4f} Nm")
    print(f"Real:     {target_real[0][0]:.4f} Nm")
    print(f"ERROR:    {diff:.4f} Nm")
    
    if diff < 0.1:
        print("✅ ¡EXCELENTE! Precisión suficiente para control.")
    else:
        print("⚠️ Aún se puede mejorar. Intenta grabar más datos.")