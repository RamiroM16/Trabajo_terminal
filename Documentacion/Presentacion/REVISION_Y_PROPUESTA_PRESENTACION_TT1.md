# Revisión del avance y propuesta para la defensa de TT1

Fecha: 7 de octubre de 2026. Tiempo disponible confirmado: 20 minutos, sin preguntas.

**Actualización:** las recomendaciones de estructura y guion de este informe se ajustaron tras recibir las observaciones del asesor. La propuesta vigente está en [AJUSTES_PRESENTACION_OBSERVACIONES_ASESOR.md](AJUSTES_PRESENTACION_OBSERVACIONES_ASESOR.md). El prompt de marco visual y las recomendaciones de legibilidad se conservan; la lámina de objetivos TT2 se retira del guion principal.

Se revisaron visualmente las 15 diapositivas de `/home/ramiro/Downloads/presentacion.pdf` y se contrastó su contenido con el TT1 corregido. El PDF original se conserva intacto. Este archivo contiene una propuesta, no una presentación ya modificada.

## Dirección de la exposición

El argumento principal es: se implementó y caracterizó en simulación un predictor de torque total con RNEA como entrada; la cuantización dinámica redujo el tamaño del archivo y la latencia media de inferencia observada, mientras el error de seguimiento aumentó y RF-01 quedó sin alcanzar.

Actualmente las diapositivas 4–10 concentran siete láminas en formatos y redes. Hay repetición, mientras faltan resultados consolidados, cumplimiento y conclusiones. Reorganizar alrededor de problema → arquitectura → implementación → condiciones experimentales → resultados → límites → TT2. No convertir la defensa en una clase larga de representación binaria.

## Revisión de las 15 diapositivas actuales

| Actual | Acción propuesta | Corrección concreta |
|---|---|---|
| 1. Portada | Conservar y limpiar | Acentos: posición, Díaz, Mecatrónica. Incluir «Trabajo Terminal I». Conservar nombres y cargos aportados; cotejarlos con los datos oficiales de la defensa, sin inferir cambios. Reducir la diagonal blanca para aprovechar espacio. |
| 2. Problema | Reescribir | Eliminar «un manipulador debe operar a 100 Hz». Sustituir por «En este proyecto: control interno nominal a 500 Hz; referencias y recopilación a 100 Hz». Describir recursos y evaluación del compromiso precisión/costo; el consumo no se midió. Título sugerido: «Problema y alcance de TT1». |
| 3. Metas | Reducir y actualizar | Agrupar en implementación en simulación, entrenamiento/quantización y comparación. No presentar solamente acciones futuras si ya se realizaron. La referencia incluye maestro RNEA + PD y predictor FP32. El texto oficial de objetivos permanece como referencia; la agrupación es para exposición. |
| 4. IEEE 754 | Unir con 5 u ofrecer como respaldo | No dedicar una lámina a decodificar −248.75 salvo pregunta. Explicar resolución finita y 32 frente a 8 bits; algunos tensores del grafo permanecen flotantes. Reutilizar paneles corregidos, no la captura genérica sin fuente. |
| 5. Cuantización | Sustituir | La imagen cambia separación temporal de barras y puede confundir muestreo con cuantización de amplitud. Usar un panel de distribucion_cuantizacion_int8_tt1_corregida_v2.png con escala, punto cero y niveles representables. Identificarlo como ejemplo conceptual. |
| 6. Redes cuantizadas | Fusionar con resultados de tamaño | Los tamaños 0.08/0.02 Mb son del ejemplo externo, no del proyecto, y Mb no equivale a MB. Sustituir por 1232 KB → 315 KB, reducción 74.43%. Mantener la misma topología antes/después: cuantizar no significa eliminar neuronas. |
| 7. Archivos reales | Reemplazar por comparativa editable | La captura muestra 1.2 MB y 322.3 kB; no puede combinarse directamente con 1232/315 KB sin cotejar archivo, bytes y convención de unidades. No afirmar que la captura es falsa. Usar valores de campaña confirmados y etiquetar «tamaño del archivo ONNX»; no memoria RAM/flash consumida. La captura puede permanecer como respaldo con sus unidades originales. |
| 8. Proceso de cuantización | Fusionar con 5 | La campana no acredita que los pesos del modelo tengan distribución normal. Usar el mapeo uniforme corregido, evitando porcentajes, histogramas o concentración de pesos no medidos. |
| 9. MLP genérica | Sustituir | Usar la topología real 42–256–512–256–128–6. Indicar ReLU, 307,590 parámetros y salida de seis torques totales después de desnormalización. |
| 10. Grafo ONNX | Pasar a respaldo | La captura es pequeña y muestra un nodo Dropout con training_mode=true. Esto no demuestra por sí solo que el artefacto de inferencia evaluado ejecutara Dropout, pero obliga a identificar versión y modo del grafo antes de usarla como evidencia de despliegue. No afirmar que Dropout está activo en operación; se describe como parte del entrenamiento. |
| 11. Control analítico | Conservar la idea y redibujar con claridad | El esquema distingue PD en torque y dinámica inversa; coincide conceptualmente con el maestro RNEA + PD. Mostrar τ_maestro=RNEA(q,dq,ddq_des)+Kp e+Kd de. No sustituirlo por el CTC ideal, que introduce el PD dentro de la aceleración de comando. |
| 12. Control neuronal | Sustituir por figura corregida simplificada | La idea de RNEA como entrada y torque total es correcta. Incorporar normalización, desnormalización, saturación provisional y tasas nominales. No añadir sumador RNEA+NN. La aceleración actual se fija a cero en despliegue. |
| 13. Metodología | Corregir flujo y reducir texto | «PyTorch → exportación ONNX → PTQ dinámica → inferencia C++». No incluir calibración estática de activaciones como procedimiento realizado. Eliminar «asegurar compatibilidad con hardware embebido». ONNX Runtime ofrece herramientas de cuantización y motor de inferencia; son etapas distintas. Usar pasado para trabajo realizado. |
| 14. Experimento | Dividir condiciones de resultados | Latencia aislada no garantiza tiempo real. Tamaño del archivo no valida memoria flash de una plataforma no implementada. Omitir consumo energético como resultado de TT1; dejarlo en trabajo futuro. Comparar analítico, FP32 e INT8 en simulación, con trayectorias quínticas y tasas diferenciadas. |
| 15. Plataforma | Adelantar y enfocar | «Entorno de simulación UR3e» describe mejor la captura que «caracterización» si no se muestran parámetros medidos. Dar protagonismo al robot, reducir consola y escritorio. Los números instantáneos visibles no sustituyen estadísticas agregadas. Si se usa video, seleccionar un fragmento breve disponible y mantener una captura como respaldo. |

## Secuencia propuesta: 18 diapositivas

Guion estimado de 18 min 45 s, dejando 1 min 15 s de margen dentro de los 20 minutos. El margen cubre cambios de diapositiva, pausas y una explicación que se alargue; no está asignado a preguntas.

| Nueva | Título | Contenido central | Recurso | Tiempo |
|---|---|---|---|---|
| 1 | Control de posición de robot manipulador usando redes neuronales cuantizadas | Identificación institucional y TT1 | Portada actual depurada | 0:30 |
| 2 | Problema y alcance | Evaluar costo de inferencia y seguimiento en simulación; implementación física posterior | Esquema CPU/memoria opcional simplificado | 1:00 |
| 3 | Objetivos de TT1 | Implementar, entrenar/cuantizar y comparar | Tres objetivos breves | 0:45 |
| 4 | Entorno de simulación | UR3e, Gazebo Harmonic, ROS 2 Jazzy y ros2_control; CPU | Captura del proyecto | 1:00 |
| 5 | Requisitos de evaluación | RMSE <0.05 rad; reducción ONNX ≥50%; 500 Hz nominal y datos 100 Hz | Tabla de tres o cuatro filas | 0:45 |
| 6 | Controlador maestro RNEA + PD | Fuente de etiquetas de torque total y referencia analítica | Diagrama del maestro y una ecuación | 1:15 |
| 7 | Arquitectura del predictor de torque total | RNEA entra a la red; desnormalización y saturación; realimentación | Figura funcional simplificada | 1:30 |
| 8 | Red neuronal implementada | 42–256–512–256–128–6; ReLU; 307,590 parámetros; seis salidas | Panel superior de la red corregida | 1:15 |
| 9 | Datos y entrenamiento | 42 entradas y 6 objetivos; normalización; aceleración filtrada en entrenamiento y cero en despliegue | Flujo de datos breve | 1:15 |
| 10 | Cuantización dinámica | Pesos fuera de línea, parámetros de activación durante inferencia; FP32/INT8 | Ruta A PTQ y un ejemplo de mapeo | 1:15 |
| 11 | Condiciones de comparación | Tres controladores; trayectorias quínticas; recopilación 100 Hz; métricas observadas | Perfil quíntico y condiciones breves | 1:15 |
| 12 | Tamaño del archivo ONNX | 1232 → 315 KB; reducción 74.43% | Dos barras desde cero y cifras legibles | 0:45 |
| 13 | Latencia de inferencia | FP32 37.1 → INT8 29.2 µs; reducción 21.29% | Dos barras desde cero y alcance «inferencia aislada» | 1:15 |
| 14 | Error de seguimiento | Analítico 0.063, FP32 0.092 e INT8 0.138 rad; umbral 0.05 rad | Tres barras desde cero y línea del requisito | 1:30 |
| 15 | Compromiso observado | Menor tamaño/latencia de inferencia junto con mayor RMSE reportado | Tabla pequeña de tres métricas | 1:00 |
| 16 | Cumplimiento y limitaciones | RF-01 no alcanzado; reducción lograda; jitter/ciclo total por verificar; límite provisional | Matriz de cuatro filas | 1:00 |
| 17 | Siguiente etapa: TT2 | Mejorar RMSE; evaluar QAT/señales; medir ciclo/jitter; preparar transferencia física | Tres o cuatro acciones agrupadas | 0:45 |
| 18 | Conclusiones | Integración en simulación; reducción observada; precisión pendiente | Tres conclusiones breves | 0:45 |

Las láminas 12–15 se pueden reducir a tres si el ensayo supera los 20 minutos. La tabla de compromiso puede integrarse a conclusiones; no se debe suprimir RF-01 ni ocultar la degradación observada.

### Texto breve reutilizable

**Problema:** «Se evalúa si la cuantización dinámica reduce el tamaño del modelo y la latencia de inferencia, conservando un desempeño de seguimiento adecuado en un UR3e simulado».

**Arquitectura:** «La red recibe RNEA como una de sus entradas y aprende el torque total del maestro RNEA + PD. Su salida se desnormaliza y se satura antes de aplicarse a la planta simulada».

**Latencia:** «Bajo la configuración experimental, la media de inferencia pasó de 37.1 a 29.2 µs. Esta medición no representa el tiempo completo del controlador».

**Precisión:** «Se reportaron RMSE de 0.063, 0.092 y 0.138 rad. Ninguna configuración alcanzó el requisito menor a 0.05 rad; estos valores son la referencia para TT2».

**Conclusión:** «Se implementó y caracterizó la arquitectura en simulación. INT8 redujo el tamaño del archivo y la latencia media de inferencia observada; mejorar la precisión de seguimiento permanece como objetivo de la siguiente etapa».

## Figuras existentes que conviene aprovechar

Ruta base: `Documentacion/TT1/Imagenes/`, enlazada a recursos compartidos. No sobrescribir originales para adaptar diapositivas.

- `diagrama_funcional_torque_total_tt1_corregida.png`: recurso principal para arquitectura. En exposición conviene ampliarlo o simplificar textos secundarios; una figura completa reducida puede resultar ilegible. Mantener RNEA → predictor → desnormalización → saturación → planta y realimentación.
- `arquitectura_red_cuantizada_tt1_corregida_v2.png`: reutilizar sólo el panel superior para topología. Los formatos inferiores van a una diapositiva específica o a respaldo, no junto con toda la red en una sola lámina.
- `distribucion_cuantizacion_int8_tt1_corregida_v2.png`: usar un panel para explicar escala/punto cero; el otro puede acompañar una pregunta. Son ejemplos de rango reducido, no parámetros del modelo.
- `comparativa_ptq_qat_tt1_corregida.png`: ruta A para metodología TT1; ruta B para trabajo futuro o respaldo. No dar a QAT el mismo protagonismo que al procedimiento realmente evaluado.
- `diagrama_flujo_rnea_tt1_corregida.png`: respaldo o síntesis visual, sin leer sus siete bloques. La latencia anotada es RNEA + PD integrado.
- `bloques_control_par_calculado_tt1_corregida.png`: sólo respaldo teórico para distinguir CTC ideal de implementación; no usarlo como diagrama del maestro real.
- `perfil_quintico_c2.png`: útil para condiciones de prueba. Es ilustración matemática, no una trayectoria registrada del ensayo.
- `arquitectura_von_neumann_cuello_botella_tt1_corregida.png`: opcional para problema; el panel de resultados no debe anticipar todas las cifras ni dominar la motivación. Evitar repetir la misma imagen completa.
- `metodologia_scrum_mecatronica_tt1_corregida.png`: respaldo si se pregunta por metodología de desarrollo; no indispensable en el guion principal de 20 minutos.

No usar la antigua figura de distribución de latencias ni el presupuesto temporal retirado del documento. Para resultados, crear barras/tablas con las métricas confirmadas; no generar trayectorias, histogramas o datos de ensayo con Gemini.

## Criterios visuales

Conservar un acento azul/gris del avance, pero retirar diagonales gruesas, sombras y franjas que ocupan espacio útil. Fondo claro en contenido: las figuras del documento ya tienen fondo blanco y colores técnicos. Portada oscura opcional con la misma identidad; no cambiar de estilo en cada lámina.

Formato 16:9, títulos en el mismo punto de anclaje y numeración uniforme. Una familia sans serif disponible en Canva, con títulos de 32–40 pt, cuerpo de 24–28 pt y fuentes/aclaraciones de al menos 16–18 pt. Son valores de diseño propuestos; comprobar en proyección. Evitar títulos enteros en mayúsculas y texto con espaciado excesivo.

Código de color propuesto: analítico azul #1D4ED8, FP32 turquesa #0F766E e INT8 ámbar #B45309. Mantener etiquetas explícitas además del color. Marcar «No alcanzado» y «Por verificar» con texto; no depender sólo de rojo/verde. Gráficas con unidades, ejes desde cero y sin efectos 3D.

Las imágenes generadas no deben contener todo el texto de las diapositivas. El marco debe ser un fondo reutilizable y el contenido debe añadirse como texto/diagramas editables en Canva. Para adaptar una figura, conservar su semántica y revisar las etiquetas después de generar.

## Prompt para Gemini: marco uniforme reutilizable

Adjuntar una diapositiva actual como referencia de paleta, indicando que se desea simplificarla. Este prompt solicita un fondo de contenido, no que Gemini invente o rehaga la exposición completa.

```text
Genera un fondo maestro reutilizable para una presentación académica de defensa de Trabajo Terminal I, Ingeniería Mecatrónica, UPIITA–IPN. Tema: control de posición de un robot UR3e simulado mediante un predictor neuronal de torque total y cuantización dinámica INT8.

Formato horizontal 16:9, 1920×1080 píxeles. Estilo técnico sobrio y uniforme, pensado para colocar encima texto editable, diagramas científicos de fondo blanco, tablas y gráficas. Fondo blanco cálido #F8FAFC; acento azul gris oscuro #263445; línea secundaria turquesa #0F766E. Conserva la sobriedad azul/gris de la referencia, simplificando su geometría.

Crear una franja superior discreta de máximo 4% de altura y un detalle geométrico mínimo en una esquina. Reservar libre la zona del título, aproximadamente x=96…1824, y=70…180. Reservar libre la zona principal x=96…1824, y=220…960. Dejar una franja inferior muy discreta para numeración y fuente, que agregaré yo. Mantener el mismo lenguaje geométrico para todas las láminas. La temática se expresa sólo mediante trazos muy tenues y abstractos de conexiones o ejes mecánicos, exclusivamente fuera del área principal.

No incluir textos, letras, números, títulos, logotipos ni marcas de agua. No incluir robots inventados, cerebros, chips, fórmulas, gráficas, métricas, brillos, efectos 3D, sombras fuertes o diagonales grandes. El centro debe permanecer completamente limpio y con alto contraste. No dibujar recuadros de contenido: debe admitir una imagen grande, dos columnas o una tabla sin cambiar el fondo.

Entregar sólo el fondo maestro, llamado marco_presentacion_tt1_16x9.png. No generar diapositivas ni resultados científicos.
```

Portada: mantener la misma paleta y detalle geométrico, con fondo #263445, amplio espacio para título blanco y datos institucionales añadidos manualmente. Si se pide variante a Gemini, cambiar sólo esta indicación; no introducir otra temática.

## Prompts opcionales para adaptar figuras a exposición

### Arquitectura funcional simplificada

```text
Adjunto el diagrama funcional corregido del proyecto. Prepara una versión para una diapositiva 16:9, manteniendo su arquitectura y paleta sobre fondo blanco. Mostrar cinco funciones principales: referencias articulares a 100 Hz; cálculo RNEA; predictor de torque total FP32/INT8; desnormalización y saturación provisional ±55 N·m en simulación; planta UR3e virtual. El cálculo RNEA alimenta al predictor como parte de sus 42 entradas; no sumar RNEA a la salida de la red. Mostrar realimentación de posición y velocidad, y recinto “Control interno nominal: 500 Hz”. Indicar con nota breve “Aceleración actual fijada a cero en despliegue”. En una nota separada: “Entrenamiento: torque objetivo del maestro RNEA + PD”. Conservar desnormalización después de la red y antes de saturación. Reducir textos secundarios, sin eliminar señales necesarias ni inventar garantías. No mostrar al UR3e físico como implementación actual. No agregar latencias, resultados o claims de seguridad. Usar etiquetas grandes, sin fórmulas largas ni bloques de código. Exportar arquitectura_control_presentacion_tt1.png.
```

### Flujo PTQ de TT1

```text
Adjunto la figura PTQ/QAT corregida. Genera sólo la ruta implementada en TT1, horizontal y legible: entrenamiento PyTorch FP32 → exportación ONNX → cuantización de pesos fuera de línea (PTQ dinámica) → inferencia C++ con ONNX Runtime. En el último bloque indicar “Escalas y puntos cero de activaciones calculados durante la inferencia”. Título: “Cuantización dinámica aplicada en TT1”. No mostrar calibración estática de activaciones, reentrenamiento QAT ni compatibilidad embebida garantizada. Fondo blanco, misma paleta técnica, máximo cuatro bloques. Mantener términos y etapas correctos; no inventar métricas. Exportar flujo_ptq_presentacion_tt1.png.
```

## Material de respaldo y comprobaciones antes de exponer

- Separar referencia teórica CTC de maestro RNEA + PD y de predictor de torque total.
- Mantener disponibles la fórmula de cuantización, el conteo de parámetros y la configuración de entrenamiento: ReLU, Dropout 0.05 tras la segunda capa densa en entrenamiento, 500 épocas configuradas, Adam 0.002 y scheduler con paciencia 15.
- No presentar 50,000 filas, N=300,000 o registros específicos como conteos trazables hasta cotejarlos. Las tasas por duración dan conteos nominales, no efectivos. El RMS impreso en un instante no sustituye una métrica temporal agregada.
- No usar P95/P99 FP32, consumo eléctrico, jitter o duración total del controlador neuronal como resultados confirmados. No sumar intervalos de cronometraje incompatibles.
- Si aparece 151.2 µs, identificarlo como controlador RNEA + PD integrado. Para comparación principal de inferencia usar FP32 37.1 e INT8 29.2 µs; el cociente frente al controlador analítico completo no acredita aceleración global.
- Conservar el límite uniforme ±55 N·m como simplificación provisional de simulación. Límites por articulación y política de fallo quedan para implementación física.
- Mostrar RF-01 no alcanzado con sus tres valores y evitar atribuir causalidad completa del error a cuantización o aceleración omitida sin ensayos controlados.
- Añadir fuentes breves de las figuras: «Elaboración propia, TT1» sólo cuando corresponda. Las capturas externas requieren su procedencia. Gemini adapta ilustraciones; no constituye fuente de resultados experimentales.
- Ensayar a 18:45 y mantener una versión que funcione sin video ni internet. La presentación final sigue pendiente de elaboración y revisión visual.
