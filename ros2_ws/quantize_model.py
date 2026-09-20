import onnx
from onnx import shape_inference
from onnxruntime.quantization import quantize_dynamic, QuantType
import os

model_path = 'ur3_neural_controller.onnx'
output_path = 'ur3_neural_controller_quantized.onnx'

print(f"--- Iniciando proceso de limpieza para {model_path} ---")

# 1. Cargar el modelo
model = onnx.load(model_path)

# 2. LIMPIEZA: Eliminar información de formas previa que causa conflicto
# Esto borra las etiquetas de '42' o '256' que están chocando
while len(model.graph.value_info) > 0:
    model.graph.value_info.pop()

# 3. RE-INFERIR: Calcular las formas correctamente
try:
    inferred_model = shape_inference.infer_shapes(model)
    onnx.save(inferred_model, 'temp_clean.onnx')
    print("✅ Metadatos de formas limpiados y regenerados.")
except Exception as e:
    print(f"⚠️ Nota: No se pudo inferir formas, pero intentaremos cuantizar igual: {e}")
    onnx.save(model, 'temp_clean.onnx')

# 4. CUANTIZACIÓN: Ahora sí, cuantizar el modelo limpio
print("Iniciando cuantización dinámica a INT8...")
quantize_dynamic(
    model_input='temp_clean.onnx',
    model_output=output_path,
    weight_type=QuantType.QInt8
)

# 5. Limpieza de archivos temporales
if os.path.exists('temp_clean.onnx'):
    os.remove('temp_clean.onnx')

# 6. Comparativa de peso
size_fp32 = os.path.getsize(model_path) / 1024
size_int8 = os.path.getsize(output_path) / 1024
print(f"\n🚀 ¡ÉXITO! Modelo cuantizado: {output_path}")
print(f"📊 Tamaño Original: {size_fp32:.2f} KB")
print(f"📊 Tamaño INT8: {size_int8:.2f} KB (Reducción del {100-(size_int8/size_fp32*100):.1f}%)")