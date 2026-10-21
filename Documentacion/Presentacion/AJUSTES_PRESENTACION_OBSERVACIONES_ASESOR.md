# Ajustes de presentación a partir de la revisión del asesor

7 de octubre de 2026. Exposición de TT1: 20 minutos, sin preguntas.

Se incorpora el resumen de la conversación con el asesor como contexto de la presentación. No se asume que su transcripción sea literal ni que todas sus expresiones técnicas estén completas. Este documento actualiza la propuesta anterior; no modifica TT1, la presentación original ni el pipeline ML.

## Cambios de estructura que se incorporan

- Portada con título oficial, identificación TT1, carrera, clave del trabajo y nombres/cargos oficiales. La portada actual ya incluye varios datos; cotejar antes de agregar o cambiar personas.
- Índice inmediatamente después de portada y antes de «Descripción del problema».
- Título exacto «Descripción del problema». «Cuello de botella computacional en plataformas con recursos limitados» puede ser una viñeta contextual; no se debe afirmar que el bus del experimento se midió saturado.
- Una diapositiva exclusivamente de objetivo general, seguida de «Objetivos específicos a cumplir en TT1».
- Títulos «Marco teórico: ...» para ordenar IEEE 754/enteros, cuantización, redes y ONNX.
- Introducir ONNX antes de presentar archivos y resultados de tamaño. Explicar primero la topología conceptual real, después su representación como grafo; el grafo detallado puede ser respaldo si resulta ilegible.
- Diagramas en fondo claro y etiquetas oscuras. Reutilizar figuras corregidas y simplificarlas para proyección.
- Citas [n] en figuras externas y conceptos fundamentados; diapositiva final de referencias completas. Usar fuentes verificadas, sin atribuir resultados experimentales a Gemini.
- Retirar la diapositiva dedicada a objetivos TT2 de la propuesta anterior. En conclusiones sólo identificar pendientes de TT1; no presentar un programa completo de la siguiente etapa.

## Precisiones técnicas al interpretar el resumen

### 1. Representaciones de 8 bits

El resumen utiliza «sin signo (INT8)». La denominación sin signo es UINT8: 0…255. INT8 con signo en complemento a dos representa −128…127. Ambos formatos tienen 256 estados; el rango físico reconstruido depende de escala S y punto cero Z, no es necesariamente −128…127 N·m.

En la lámina principal conviene comparar FP32 con INT8 con signo, coherente con los pesos QInt8 descritos en el proyecto. Se puede añadir una nota breve sobre UINT8 si se explica la cuantización de activaciones, cuyo tipo efectivo depende del grafo. No afirmar que todos los tensores y operaciones del modelo se convierten a enteros.

### 2. Número de niveles y resolución

Para B bits, el número de códigos posibles es L=2^B, no 2B. Para B=8, L=256. En un ejemplo uniforme que incluye ambos extremos xmin y xmax como niveles, la separación es Δ=(xmax−xmin)/(L−1). Esta fórmula requiere especificar esa convención de extremos; otros esquemas de intervalos pueden definir la resolución de otra forma.

Para el modelo afín, usar la fórmula más general S=(xmax−xmin)/(qmax−qmin), junto con q=clip(round(x/S)+Z,qmin,qmax) y x_hat=S(q−Z). La escala S es la separación entre valores reales reconstruidos consecutivos. En mapeos simétricos se debe respetar la convención del rango y la representación exacta del cero.

### 3. Distribución normal frente a uniforme

Distinguir la distribución de los datos de la distribución de niveles del cuantizador. Un histograma aproximadamente normal puede influir en la selección de escala, rango o criterio de calibración. Sin embargo, un cuantizador uniforme conserva pasos equidistantes: una campana no cambia automáticamente ese espaciado.

Asignar pasos más pequeños a zonas de mayor densidad exige un cuantizador no uniforme u otro procedimiento específicamente definido. No se aplicó ni se verificó ese método en TT1. No presentar como resultado «la distribución normal asigna mejor los niveles» ni simular una campana y llamarla histograma del modelo.

Para responder a la intención didáctica del asesor, explicar escala y rango con la figura corregida y preparar como respaldo una comparación conceptual de distribuciones, rotulada como ilustración. No hacer de normalidad frente a uniformidad un resultado de este proyecto ni afirmar superioridad sin definir el criterio de error y el cuantizador.

Fuente primaria del método aplicado: https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html . ONNX Runtime describe cuantización lineal de 8 bits y, en su modalidad dinámica, cálculo de parámetros de activación durante la inferencia.

### 4. ONNX e interoperabilidad

Texto sugerido: «ONNX es una representación abierta de modelos mediante grafos, operadores y tensores. Permite intercambiar modelos entre herramientas compatibles. En este proyecto se utiliza para exportar desde PyTorch y ejecutar inferencia con ONNX Runtime en C++».

No afirmar que exportar ONNX garantiza ejecución en cualquier FPGA o sistema embebido. Se requiere soporte de operadores, tipos de datos, runtime/backend y recursos de cada plataforma. El experimento de TT1 se describe como ejecución en CPU.

Fuente primaria: https://onnx.ai/onnx/intro/concepts.html .

### 5. Aceleración actual fijada a cero

La observación del asesor se conserva como un punto técnico que debe explicarse. El estado real es: la aceleración actual se obtiene por procesamiento de señales en entrenamiento y se fija a cero durante el despliegue. Esto crea una diferencia entre las características de ambos dominios.

Texto recomendado para exposición:

> «Durante el despliegue se fijó la aceleración actual a cero como simplificación de la preparación de entradas. Estimar aceleración a partir de posición requiere diferenciación y filtrado; en TT1 no se integró ese estimador al controlador. Esta elección introduce una diferencia respecto al entrenamiento, por lo que se reconoce como limitación. Su efecto sobre el seguimiento requiere ensayos controlados».

No presentar «evita el ruido» como un beneficio demostrado, ni afirmar que todas las plataformas robóticas carecen de sensores de aceleración. Las interfaces utilizadas proporcionan posición y velocidad; no debe extrapolarse esa configuración a todo robot.

Eliminar seis entradas de aceleración actual daría 36 entradas en lugar de 42. Requeriría reentrenar y actualizar topología, escaladores, exportación e integración. Evaluar un modelo sin esas entradas es una propuesta de experimento, no una modificación ya realizada ni una explicación probada del RMSE. Se respeta la decisión de no modificar ahora el pipeline.

## Objetivos: texto y alcance

El objetivo general disponible en TT1 es:

> «Evaluar el desempeño energético, de precisión y de recursos utilizados en la implementación de un control de lazo cerrado con una planta robótica con control tradicional y con una red neuronal cuantizada».

Mantenerlo como objetivo declarado; no sustituirlo silenciosamente por uno que coincida sólo con lo completado. En la explicación del alcance señalar: en TT1 se caracterizaron seguimiento, tamaño del archivo y latencia de inferencia en simulación; la evaluación eléctrica directa no se realizó.

Los objetivos específicos del documento incluyen una metodología con al menos dos niveles de precisión y un plan de comparación energética. La campaña documentada compara FP32 e INT8; no acredita evaluación de dos anchos enteros, como INT6 e INT8. Presentar objetivos y avances con ese alcance, sin declarar cumplimiento total de todos ellos. Esta es una cuestión de trazabilidad que debe aclararse con el asesor; no se altera el protocolo ni se inventa una campaña adicional.

Para la lámina de objetivos específicos, agrupar de forma fiel en investigación, arquitectura/control base, metodología de cuantización y plan experimental/plataforma. Las formulaciones completas pueden estar en respaldo. La diapositiva de cumplimiento explica qué se ejecutó y qué permanece pendiente.

## Guion actualizado para 20 minutos

22 láminas, con varias de transición muy breves. Tiempo previsto: 18:50; margen: 1:10. No deben leerse las referencias, el índice ni todos los bits del formato. Si el ensayo supera el tiempo, reducir la explicación del grafo y fusionar condiciones del entorno con experimento; conservar las láminas separadas de objetivos solicitadas por el asesor.

| N.º | Título | Contenido o recurso | Tiempo |
|---|---|---|---|
| 1 | Portada | Datos institucionales y del trabajo | 0:30 |
| 2 | Índice | Problema/objetivos; marco teórico; diseño e implementación; evaluación; conclusiones | 0:20 |
| 3 | Descripción del problema | Recursos de cómputo, necesidad de comparación y alcance en simulación | 0:50 |
| 4 | Objetivo general | Texto declarado, sin atribuir cumplimiento a toda su evaluación | 0:35 |
| 5 | Objetivos específicos a cumplir en TT1 | Agrupación fiel al documento; no objetivos TT2 | 0:45 |
| 6 | Marco teórico: FP32 e INT8 | 32/8 bits, representación finita; signo y escala; nota UINT8 si hace falta | 1:00 |
| 7 | Marco teórico: cuantización | L=2^B, escala S, punto cero Z y ejemplo conceptual corregido | 1:05 |
| 8 | Marco teórico: redes neuronales | Concepto MLP y diferencia entre cuantización y reducción de neuronas | 0:40 |
| 9 | Marco teórico: ONNX | Grafo abierto y papel de exportación/runtime en este proyecto | 0:40 |
| 10 | Entorno de simulación | UR3e, Gazebo, ROS 2 y CPU; 500 Hz nominal/100 Hz datos | 0:45 |
| 11 | Controlador maestro RNEA + PD | PD en torque, etiquetas de torque total; diagrama claro | 1:05 |
| 12 | Topología de la red implementada | 42–256–512–256–128–6; ReLU; Dropout en entrenamiento; parámetros | 1:00 |
| 13 | Arquitectura del predictor de torque total | RNEA como entrada, normalización, salida, desnormalización, saturación | 1:20 |
| 14 | Datos y tratamiento de la aceleración | Entrenamiento/despliegue; simplificación y limitación reconocida | 1:15 |
| 15 | Cuantización dinámica implementada | PyTorch → ONNX → cuantización de pesos → inferencia; activaciones dinámicas | 1:00 |
| 16 | Condiciones y métricas de comparación | Analítico/FP32/INT8; trayectorias quínticas; alcance de mediciones | 1:00 |
| 17 | Tamaño del archivo ONNX | 1232→315 KB, reducción 74.43%; no memoria total de ejecución | 0:45 |
| 18 | Latencia de inferencia | 37.1→29.2 µs, reducción 21.29%; no tiempo total ni garantía temporal | 1:00 |
| 19 | Seguimiento articular | 0.063/0.092/0.138 rad; línea del criterio <0.05 rad | 1:20 |
| 20 | Cumplimiento y limitaciones | RF-01 no alcanzado; compresión observada; ciclo/jitter y energía pendientes | 1:00 |
| 21 | Conclusiones de TT1 | Implementación, resultados comparativos y límites del alcance | 0:45 |
| 22 | Referencias | Fuentes citadas completas; dejar disponible al terminar | 0:10 |

## Figuras y bibliografía

Se mantienen las recomendaciones de reutilización del informe previo: topología real, figura funcional corregida, ruta PTQ y cuantización v2. No insertar las láminas completas del documento con letra diminuta. Rediseñar o ampliar paneles específicos para proyección.

El diagrama maestro actual representa RNEA + PD en torque; no reemplazarlo por el CTC teórico. La figura neuronal debe mantener RNEA como entrada y salida total, sin sumador residual.

Enumerar [1], [2]… según su primera aparición y comprobar correspondencia exacta con referencias finales. Para conceptos ONNX/ONNX Runtime se pueden usar las fuentes oficiales anteriores; para RNEA y redes utilizar referencias ya verificadas del reporte. No conservar ilustraciones externas sin identificar su procedencia. Una figura propia puede rotularse «Elaboración propia» y citar la fuente teórica que fundamenta el concepto cuando corresponda.

## Ajuste del prompt visual para Gemini

El prompt del marco uniforme sigue siendo utilizable: fondo claro, paleta azul/gris y turquesa, 16:9, centro limpio y contenido añadido en Canva. Agregar esta instrucción al encargo de composición de diapositivas, sin pedir que forme parte del fondo vacío:

> «Mantener una zona consistente para título de sección y una zona inferior para citas numeradas [n]. Las secciones del marco teórico deben titularse “Marco teórico: [tema]”. Incluir layouts para índice, objetivo general, objetivos específicos, diagramas, resultados y referencias. No generar contenido científico ni referencias automáticamente. El fondo maestro no debe incluir palabras o números; estos se añadirán como elementos editables».

El cambio de estructura no requiere otro estilo visual ni volver a generar las imágenes corregidas de TT1. La presentación editable y su revisión final permanecen pendientes de elaboración.
