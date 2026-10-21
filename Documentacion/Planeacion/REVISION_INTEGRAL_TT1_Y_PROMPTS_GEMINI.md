# Revisión integral TT1: texto, tablas y figuras

Se revisaron las nueve imágenes incluidas en TT1, las tablas y sus interpretaciones, las configuraciones descritas frente al código y las referencias cruzadas. La revisión no equivale a reproducir la campaña ni a verificar individualmente toda la bibliografía.

## Correcciones documentales realizadas

- Entrenamiento coherente con el código, confirmado por el autor: ReLU, Dropout 0.05 después de la segunda capa densa, 500 épocas, Adam con tasa 0.002 y scheduler con paciencia 15. Se retira la afirmación de ausencia de sobreajuste.
- P95/P99 FP32 y mejoras relativas omitidos por decisión del autor hasta recuperar los registros. Se conservan las medias, dispersiones, medianas y máximos reportados; no se inventan percentiles.
- Pugh: A suma −0.15, no −0.20; C suma 1.45. Los pesos suman 1. Se identifica como valoración conceptual, sin acreditar superioridad experimental en precisión, estabilidad o transferencia física.
- MSE coherente con nn.MSELoss(): promedio sobre muestras y seis salidas estandarizadas. La pérdida de entrenamiento no se equipara con RMSE articular en radianes.
- Se diferencia CTC teórico, con PD dentro de la aceleración de control, del código TT1, que aplica RNEA con aceleración deseada y suma PD en torque. Se retira una expresión de error no ideal inconsistente y se conserva el caso ideal bajo modelo exacto.
- Dataset: 42 entradas y 6 objetivos seleccionados, no 42 columnas totales. Las 50,000 filas siguen siendo un dato reportado por cotejar con el CSV, no un valor constante del código.
- Se deja explícita la limitación del ajuste de escaladores antes de dividir los datos; la evaluación independiente requiere revisión posterior sin modificar el pipeline ahora.
- RF-04 y matriz final comparten el criterio de reducción del archivo de al menos 50%; se conserva el resultado confirmado 74.43%.
- Se corrigen los tópicos de referencia y se retiran atribuciones de jerk continuo o validación multiaxial mediante una ecuación escalar de inercia.
- Se conserva el error estático de torque reportado sin atribuirlo a J1 o al hombro hasta confirmar los registros. Su diferencia FP32–INT8 es +0.008 N·m; se retira «Inapreciable».
- Se evita fijar el cero de activaciones a −128 por el solo hecho de que los pesos sean QInt8. Los rangos dependen del tipo de tensor del grafo.

## Imágenes: estado y prioridades

| Archivo actual | Estado | Corrección necesaria |
|---|---|---|
| arquitectura_von_neumann_cuello_botella.png | Prioridad alta | Cero asignaciones, residencia caché, consumo, holgura y 100 Hz como control ya contradicen el texto |
| diagrama_flujo_rnea.png | Prioridad alta | Atribuye 151.2 µs a RNEA aislado; recursiones deben revisarse con una convención consistente |
| arquitectura_red_cuantizada.png | Prioridad alta | LeakyReLU contradice código; DSP48E mezcla CPU con FPGA futura; FP32 no es continuo analógico; MB inconsistente |
| distribucion_cuantizacion_int8.png | Prioridad alta | Curvas sintéticas presentadas como pesos reales, 99.73% y concentración sin histograma; cuantización simétrica también es uniforme; cero de activación no necesariamente −128 |
| comparativa_ptq_qat.png | Corregir | Ruta A es PTQ estática, no dinámica utilizada; “ideal” y “maximiza” son conclusiones generales excesivas |
| bloques_control_par_calculado.png | Corregir | Es referencia teórica; RNEA/QNN no deben figurar como intercambiables con la implementación TT1 |
| metodologia_scrum_mecatronica.png | Ajuste menor | Sim-to-Real, “validada” y “optimizado” deben expresarse como objetivos o resultados evaluados |
| diagrama_funcional_torque_total.png | Ajuste menor | Arquitectura correcta; aclarar límite provisional de simulación y evitar llamar “desacoplamiento” al resultado sin prueba |
| perfil_quintico_c2.png | Conservar | Ilustra un polinomio y sus dos derivadas; no confundir con un registro de movimiento real ni con continuidad del jerk |

La imagen distribucion_latencia_m3.png y timing_budget_500hz.png NO están incluidas en el TT1 actual. La primera fue construida con datos aleatorios por su script (N=300,000); no debe reincorporarse como histograma experimental. La segunda conserva el presupuesto basado en intervalos mezclados. Se mantienen sus originales sin utilizarlos como evidencia.

## Uso de Gemini y ubicación de archivos

Adjuntar a Gemini la imagen original correspondiente y copiar su prompt. Conservar paleta, estilo, proporciones y distribución visual, pero priorizar legibilidad y exactitud. Exportar las nuevas imágenes con el sufijo `_tt1_corregida.png` en `Documentacion/TT1/Imagenes/`. Esta carpeta enlaza a recursos compartidos de Protocolo: el sufijo evita sobrescribir imágenes del protocolo aprobado. Se revisarán antes de cambiar los includegraphics; los originales permanecen intactos.

No generar nuevas métricas, histogramas, pruebas ni resultados. Las curvas didácticas deben identificarse claramente como ilustraciones conceptuales.

## Prompt 1 — Cuello de botella y cuantización

```text
Corrige la imagen adjunta conservando su apariencia, bloques, colores y estilo académico. Título: “Arquitectura Von Neumann y cuantización: contexto e indicadores observados”. En el bloque CPU–memoria presenta tráfico de datos como concepto general, sin afirmar saturación medida del bus. Sustituye el subtítulo por “Control interno nominal: 500 Hz; referencias y recopilación: 100 Hz”. Panel derecho con tres bloques:
1. “Tamaño del archivo ONNX”: FP32 = 1232 KB; INT8 = 315 KB; reducción = 74.43%. No mostrar MB ni residencia garantizada en caché.
2. “Inferencia observada en CPU”: media FP32 = 37.1 µs; media INT8 = 29.2 µs; reducción de tiempo = 21.29%, bajo la configuración experimental. No atribuirla a SIMD, AVX, área de silicio ni consumo medido.
3. “Verificaciones pendientes”: duración total del controlador neuronal, jitter del periodo y consumo eléctrico. Indicar que el código conserva asignaciones dinámicas y que el despliegue físico es trabajo de TT2. Eliminar cero asignaciones, holgura garantizada, viabilidad embebida demostrada y la regla de 100 Hz como bucle estricto.
No añadir resultados ni garantías. Exportar arquitectura_von_neumann_cuello_botella_tt1_corregida.png.
```

## Prompt 2 — Flujo RNEA

```text
Corrige la imagen adjunta manteniendo sus dos columnas y bloques de color: pasada hacia adelante y pasada hacia atrás. Debe ser un diagrama ALGORÍTMICO CONCEPTUAL, no una validación de las ecuaciones del código. Sustituye las fórmulas detalladas de recursión por pasos descriptivos para evitar mezclar convenciones de marcos: condiciones de base y gravedad; propagación de velocidad/aceleración; aceleración del centro de masa; fuerzas y momentos inerciales; transmisión de fuerzas del extremo a la base; transmisión de momentos; proyección del momento sobre el eje articular. Conserva salida τ_RNEA y complejidad O(n). Corrige el orden visual de la pasada hacia atrás: paso 5 → paso 6 → paso 7, con flechas inequívocas. Elimina “Cálculo eficiente en C++ (151.2 µs en UR3e)” de RNEA. Si se incluye una nota de latencia, debe decir exactamente “151.2 µs: media reportada del cálculo RNEA + PD integrado; no corresponde a RNEA aislado”. No añadir otra latencia, ni garantía de exactitud o estabilidad. Exportar diagrama_flujo_rnea_tt1_corregida.png.
```

## Prompt 3 — Arquitectura de red y formatos

```text
Corrige la imagen adjunta conservando las capas de colores y la organización en paneles. Red MLP: 42 → 256 → 512 → 256 → 128 → 6. Capas ocultas con ReLU, NO LeakyReLU. Dropout p=0.05 después de la segunda capa densa, sólo como parte del entrenamiento. Total EXACTO: 306,432 pesos + 1,158 sesgos = 307,590 parámetros. Pesos por transición: 10,752; 131,072; 131,072; 32,768; 768. Salida: torque total aprendido del maestro RNEA + PD. RNEA sigue como entrada; no mostrar suma residual. Aceleración actual: filtrada en entrenamiento, fijada a cero en despliegue. Límite ±55 N·m provisional uniforme para simulación; límites por articulación pendientes para TT2.
Los formatos FP32 e INT8 se ilustran conceptualmente. FP32 tiene representación finita y NO es señal continua analógica ni carece de redondeo. INT8 usa 8 bits en complemento a dos; algunos tensores del modelo cuantizado permanecen flotantes. Las curvas inferiores son ejemplos didácticos, no registros de robot ni resultados experimentales de amplitud. Rotularlas como “Ilustración conceptual de resolución numérica”. En cuadros separados indicar sólo los resultados reportados: FP32 1232 KB, media 37.1 µs, máximo observado 42.0 µs, RMSE 0.092 rad; INT8 315 KB, media 29.2 µs, máximo observado 39.0 µs, RMSE 0.138 rad. Recopilación 100 Hz y control nominal 500 Hz. Eliminar conversiones MB, ejecución AVX2/FPU, DSP48E, coprocesador, FPGA o SIMD como resultados de esta ejecución. No generar percentiles ni curvas empíricas. Exportar arquitectura_red_cuantizada_tt1_corregida.png.
```

## Prompt 4 — Cuantización: esquema conceptual correcto

```text
Rediseña la figura adjunta conservando dos paneles y la paleta azul/naranja. Debe ilustrar cuantización UNIFORME afín, no un histograma del modelo. Título general: “Cuantización uniforme afín: ejemplos conceptuales”. Panel (a): pesos con ejemplo de cuantización simétrica Z_w=0, escala S_w y niveles equidistantes; puede mostrar una función en escalones o valores antes/después. Panel (b): activaciones con ejemplo de cuantización asimétrica, escala S_a y punto cero Z_a que representan el cero real; no fijar Z_a=-128 ni afirmar un tipo de activación sólo por usar pesos QInt8. Incluir la relación x≈S(q−Z) y señalar que los parámetros efectivos dependen del grafo exportado. Si se escoge un tipo entero para el ejemplo, rotular explícitamente “ejemplo ilustrativo” y dar su rango coherente.
Eliminar campana de pesos reales, Adam+L2 como prueba de normalidad, 99.73%, “soporte útil”, colas vacías, niveles desperdiciados y “100% de niveles aprovechados”. La cuantización simétrica también es uniforme; no mostrarla como concentración no uniforme automática. No inventar histogramas ni métricas. Exportar distribucion_cuantizacion_int8_tt1_corregida.png.
```

## Prompt 5 — PTQ dinámica y QAT

```text
Corrige la comparación adjunta manteniendo dos rutas y colores. Ruta A: “PTQ dinámica — aplicada en TT1”: entrenamiento FP32 → exportación ONNX → cuantización de pesos fuera de línea → inferencia con parámetros de cuantización de activaciones calculados en ejecución. No introducir calibración estática con dataset Min-Max como paso realizado en TT1. Nota: sin reentrenamiento específico de cuantización; tamaño del archivo 1232 → 315 KB, reducción observada 74.43%. No llamarla ideal para CPU ni garantizar aceleración.
Ruta B: “QAT — propuesta para TT2”: cuantización aparente en entrenamiento → forward con simulación de redondeo → backward con estimador STE → ajuste de pesos considerando cuantización → evaluación posterior. Sustituir “pesos compensan el ruido” por “se busca reducir el efecto del error de cuantización”. Eliminar “maximiza precisión” y resultados sub-8 bits no evaluados. Indicar que QAT no se probó en TT1. No crear métricas futuras. Exportar comparativa_ptq_qat_tt1_corregida.png.
```

## Prompt 6 — CTC teórico

```text
Corrige el diagrama adjunto manteniendo su estructura de bloques y colores. Debe titularse “Control por par calculado: referencia teórica”, con una nota visible “Este esquema no representa directamente la implementación RNEA + PD de TT1”. Mostrar error de posición e=q_d−q y error de velocidad de=dq_d−dq. El PD de aceleración es Kp e+Kd de; se suma con la aceleración deseada para formar a_cmd. Dinámica inversa: τ=M_hat(q) a_cmd+c_hat(q,dq)+g_hat(q). Retirar “RNEA / QNN” como alternativas intercambiables de ese bloque. Mostrar planta y realimentación de q,dq. Indicar “Desacoplamiento ideal bajo modelo exacto”, sin afirmar estabilidad validada. Nota de TT1: τ_maestro=RNEA(q,dq,ddq_des)+Kp_torque e+Kd_torque de. No mezclar ganancias de aceleración con ganancias de torque ni mostrar la red neuronal como reemplazo de RNEA. Sin latencias ni métricas experimentales. Exportar bloques_control_par_calculado_tt1_corregida.png.
```

## Prompt 7 — Metodología

```text
Ajusta el diagrama adjunto manteniendo columnas, colores y apariencia. Presentarlo como marco metodológico adaptado, no evidencia de que cada resultado ya se certificó. Cambiar “Verificación Sim-to-Real” por “Evaluación en simulación; transferencia física prevista para TT2”. Cambiar “Plugin de control C++ optimizado” por “Plugin de control C++ implementado” y “Red cuantizada validada” por “Red cuantizada evaluada en simulación”. Usar “Registro de datos a 100 Hz” donde diga telemetría de alta frecuencia. Mantener RMSE cuantificado y avances documentados, pero no garantías de seguridad, estabilidad o despliegue físico. Las duraciones de 2–4 semanas son propuestas del marco, no un cronograma experimental verificado: rotularlas como orientativas. Exportar metodologia_scrum_mecatronica_tt1_corregida.png.
```

## Prompt 8 — Ajustes menores del diagrama funcional

```text
Conserva exactamente la arquitectura de torque total de la imagen adjunta, la disposición, colores y flechas. Ajustar sólo texto: “Control interno nominal (ros2_control, 500 Hz)” sin atribuir tiempo real estricto; RNEA produce información dinámica nominal, no “desacoplamiento” certificado; bloque de saturación “Límite uniforme provisional en simulación: ±55 N·m. Límites por articulación previstos para implementación física TT2”. En predictor, “Inferencia del modelo FP32 o cuantizado dinámicamente INT8”, sin atribuir toda la inferencia a aritmética entera. Mantener 42 entradas, topología correcta, aceleración actual fijada a cero en despliegue, salida de torque total, desnormalización y saturación; NO agregar sumador RNEA+NN. Mantener 100 Hz para referencias y datos, tópico /custom_torque_controller/command y nota de entrenamiento por imitación del maestro RNEA+PD. No introducir garantías ni nuevas métricas. Exportar diagrama_funcional_torque_total_tt1_corregida.png.
```

## Pendientes de evidencia y estructura

- Confirmar registros originales para percentiles FP32, el presupuesto por subproceso aún reportado, el número efectivo de muestras y los valores de SNR/errores estáticos y cinemáticos. La confirmación de medias de latencia y tamaños no verifica automáticamente todas esas métricas.
- Identificar versión de modelo y configuración de exportación: el script solicita opset 9, pero el análisis de artefactos registró opset 18. Se describe el script, no una equivalencia comprobada de versión.
- La consola calcula RMS sobre seis errores articulares en un instante. Las medias de seguimiento reportadas requieren identificar si se agregaron RMS instantáneos o se calculó RMSE temporal global; no modificar las cifras confirmadas sin reconstruir su cálculo.
- Revisar bibliografía contra fuentes primarias antes de sostener porcentajes energéticos y conclusiones específicas de literatura. Compilación de citas no verifica el contenido citado.
- Completar análisis de costos/valor con alcance TT1 y separar costos estimados de reales. No se inventaron costos ni un consumo eléctrico.
- Documentar evolución frente al protocolo aprobado, en especial PID/FP12/varias precisiones frente a RNEA+PD y FP32/INT8 CPU. No reescribir el protocolo.
- Revisar preliminares y extensión del resumen; la auditoría técnica no acredita cumplimiento total de formato institucional.

El listado y los ocho prompts anteriores documentan la revisión inicial. El estado de integración actualizado se registra a continuación.


## Revisión de imágenes recibidas e integración — 7 de octubre de 2026

Se inspeccionaron las ocho versiones `_tt1_corregida.png` entregadas por el autor. Se integran completas seis: cuello de botella, flujo RNEA, CTC teórico, PTQ/QAT, Scrum y arquitectura funcional. Se conserva la imagen quíntica. Se ajustan textos y pies para identificar conceptos, indicadores observados y propuestas TT2, manteniendo etiquetas y referencias cruzadas.

La figura de la red se integra sólo con el panel superior de topología, mediante recorte de visualización en LaTeX: se conserva intacto el PNG. Ese panel coincide con capas, ReLU, Dropout y conteo de parámetros. Se aclara que las seis salidas de la red son estandarizadas y el torque físico se obtiene tras desnormalizarlas. Los paneles inferiores aún llaman «magnitud» a los siete bits inferiores del complemento a dos; no representan una magnitud separada. Además, la curva dibujada no permite afirmar que reproduce 256 niveles y la fórmula FP32 requiere restringirse a números normales.

La figura de cuantización se omite temporalmente: el título del panel (b) está recortado en el propio PNG y las mesetas extremas/escala dibujadas no identifican una cuantización consistente con el rango anunciado. Se mantienen las ecuaciones y explicación de cuantización uniforme en el texto, sin utilizar histogramas ficticios ni dejar referencias pendientes.

En la figura funcional, «registro de 42 canales» describe un flujo de señales, no el número total de columnas seleccionadas del dataset: éste incluye 42 entradas y 6 objetivos. Las tasas son nominales y la saturación de ±55 N·m continúa siendo provisional en simulación. El diagrama RNEA se interpreta como resumen conceptual en marcos compatibles, no una certificación de las recursiones implementadas.

### Prompt adicional — Paneles inferiores de la red

```text
Corrige únicamente los paneles inferiores de arquitectura_red_cuantizada_tt1_corregida.png. Conserva el panel superior de topología, colores y conteos. En INT8 elimina “Magnitud entera en complemento a 2 (7 bits)”: mostrar ocho bits b7…b0 y el valor q=−128 b7+sum(i=0…6,2^i b_i), rango −128…127. El bit b7 tiene peso negativo; no hay un campo separado de magnitud. Mantener x≈S(q−Z) y nota de tensores flotantes. En FP32 indicar que v=(−1)^s 2^(e−127)(1+m) corresponde a valores normales (1≤e≤254); subnormales, cero e Inf/NaN requieren tratamiento distinto. Las curvas deben decir “ejemplo didáctico con pocos niveles visibles”; quitar “discretización en 256 niveles” si no se dibujan esos niveles. Eje horizontal “Variable ilustrativa (sin unidad)”, no tiempo de ciclo ni fase articular sin definir. No crear métricas ni curvas de movimiento real. En topología aclarar “salida estandarizada; torque N·m tras desnormalización”, sin cambiar las seis salidas ni la arquitectura de torque total. El tamaño y las métricas confirmadas se conservan. Guardar como arquitectura_red_cuantizada_tt1_corregida_v2.png.
```

### Prompt adicional — Gráfica de cuantización

```text
Corrige distribucion_cuantizacion_int8_tt1_corregida.png conservando dos paneles azul/naranja. Garantizar que TODOS los títulos, leyendas y anotaciones caben completos: acortar el título inferior a “(b) Cuantización uniforme afín de activaciones”. Dibujar matemáticamente las curvas a partir de q=clip(round(x/S)+Z,qmin,qmax) y x_hat=S(q−Z), sin inventar mesetas ni saturación fuera de esos límites. Para un ejemplo simple con pocos niveles: S=0.2, qmin=−5, qmax=5, Z=0 para el panel simétrico; S=0.25, qmin=0, qmax=8, Z=1 para el panel asimétrico. Rotular “Ejemplo didáctico con rango entero reducido; no son parámetros del modelo TT1”. Mostrar niveles equidistantes y marcar el cero real, evitando afirmar que la imagen usa todo el rango INT8 o sus 256 estados. Diferenciar valores reales ideales de valores representables. No usar porcentajes, histogramas, normalidad de pesos ni aprovechamiento óptimo. Ajustar márgenes y tamaños de letra para evitar cualquier recorte. Guardar como distribucion_cuantizacion_int8_tt1_corregida_v2.png.
```


## Cierre de integración de imágenes v2 — 7 de octubre de 2026

Se revisaron las dos versiones adicionales entregadas por el autor. La arquitectura neuronal v2 se integra completa, retirando el recorte temporal de topología. El formato INT8 muestra los ocho bits con peso −128 para b7 y ponderaciones positivas para b6…b0; las curvas se identifican como ejemplos didácticos con pocos niveles visibles y las salidas se distinguen de su torque desnormalizado. Se explicita en el texto y pie que la fracción FP32 es 0.f y el significando normal es 1.f, para evitar confundir la etiqueta de mantisa con la fracción de la fórmula.

La cuantización v2 presenta títulos completos y escalones consistentes con los parámetros ilustrativos. Se integra con su referencia cruzada y se explican los rangos reconstruidos: [−1,1] para S=0.20, Z=0, q=−5…5; [−0.25,1.75] para S=0.25, Z=1, q=0…8. Estos rangos reducidos no se atribuyen al modelo de la campaña.

Quedan integradas las ocho figuras corregidas solicitadas y se conserva la quíntica. No se alteraron los PNG originales, el protocolo, el código o las métricas confirmadas. Los pendientes de trazabilidad experimental y bibliográfica de la auditoría integral continúan vigentes.

Verificación: latexmk/pdflatex finaliza con código 0, PDF actualizado de 97 páginas, sin citas ni referencias cruzadas pendientes. Se inspeccionan las dos figuras completas y sus pies en las páginas físicas 55 y 68. git diff --check sin errores. Persisten advertencias tipográficas generales previamente registradas.
