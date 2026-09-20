import sqlite3
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
from rclpy.serialization import deserialize_message
from std_msgs.msg import Float64MultiArray
from scipy.signal import savgol_filter
import pandas as pd
import sys
import os

# --- CONFIGURACIÓN ---
BAG_FOLDER = 'dataset_ur3_final_1'  # Asegúrate de que este nombre coincida con tu carpeta
TOPIC_NAME = '/custom_torque_controller/training_data'
OUTPUT_FILE = 'dataset_ur3_final_1.csv'

# Definimos el tamaño esperado: 7 vectores de 6 valores = 42
EXPECTED_SIZE = 42 

def extract_data():
    if not os.path.exists(BAG_FOLDER):
        print(f"Error: No encuentro la carpeta '{BAG_FOLDER}'.")
        return

    storage_options = StorageOptions(uri=BAG_FOLDER, storage_id='mcap')
    converter_options = ConverterOptions('', '')
    reader = SequentialReader()
    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()
    type_map = {topic.name: topic.type for topic in topic_types}

    data_rows = []
    
    print(f"Leyendo '{BAG_FOLDER}'...")
    
    count = 0
    missed = 0
    
    while reader.has_next():
        (topic, data, t) = reader.read_next()
        
        if topic == TOPIC_NAME:
            msg = deserialize_message(data, Float64MultiArray)
            
            # --- CORRECCIÓN AQUÍ ---
            # Verificamos contra el nuevo tamaño (42)
            if len(msg.data) == EXPECTED_SIZE:
                data_rows.append(msg.data)
                count += 1
            else:
                missed += 1
                if missed == 1:
                    print(f"ALERTA: Se encontró un mensaje con {len(msg.data)} datos (se esperaban {EXPECTED_SIZE}).")

            if count % 1000 == 0 and count > 0:
                print(f"Procesados {count} muestras...", end='\r')

    print(f"\nLectura completa. Total muestras válidas: {count}")
    print(f"Muestras descartadas (tamaño incorrecto): {missed}")

    if count == 0:
        print("No se encontraron datos válidos. Verifica que el C++ esté publicando 42 valores.")
        return

    # Definir nombres de columnas (7 grupos de 6 joints)
    cols = []
    joints = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    
    # El orden debe coincidir EXACTAMENTE con el push_back del C++
    prefixes = [
        'q_act',    # 1. Posición Actual
        'dq_act',   # 2. Velocidad Actual
        'q_des',    # 3. Posición Deseada
        'dq_des',   # 4. Velocidad Deseada
        'ddq_des',  # 5. Aceleración Deseada
        'tau_rnea', # 6. Torque Modelo
        'tau_cmd'   # 7. Torque Total Enviado
    ]
    
    for pre in prefixes:
        for j in joints:
            cols.append(f'{pre}_{j}')

    # Verificación final de dimensiones
    if len(cols) != EXPECTED_SIZE:
        print(f"Error interno: Definiste {len(cols)} nombres de columna pero esperas {EXPECTED_SIZE} datos.")
        return

    df = pd.DataFrame(data_rows, columns=cols)
    
    print("Calculando aceleraciones actuales derivadas (ddq_act)...")
    dt=0.01
    joints = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    for j in joints:
        vel_col = f'dq_act_{j}'
        acc_col = f'ddq_act_{j}'
        df[acc_col] = savgol_filter(df[vel_col], window_length=11, polyorder=3, deriv=1, delta=dt)
    
    # Reordenar columnas para que ddq_act quede junto a las otras
    cols_final = df.columns.tolist()
    cols_final.sort()
    df = df[cols_final]

    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"¡Éxito! Archivo guardado como: {OUTPUT_FILE}")
    print(df.head()) # Muestra las primeras filas para verificar

if __name__ == "__main__":
    extract_data()