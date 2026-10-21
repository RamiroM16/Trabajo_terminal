# Bitácora de correcciones de TT1

## 1. Frecuencias de control, referencias y adquisición

Confirmación del autor: los datos se recopilaron siempre a 100 Hz. El generador publicó referencias a 100 Hz y el control interno estuvo configurado a 500 Hz. La atribución de 500 Hz al registro experimental fue un error introducido en la redacción.

Corrección aplicada en `Documentacion/TT1/TT1.tex`:

- Separación de periodos: control interno 2 ms; referencias y datos 10 ms.
- Eliminación de los extractos erróneos de publicación a 500.04 Hz y del bag de 300,010 mensajes; no se fabricaron capturas alternativas.
- 300,000 queda sólo como número nominal de actualizaciones internas en 600 s. A 100 Hz corresponden nominalmente 60,000 muestras por señal, sin atribuir ese conteo exacto al registro.
- Se mantiene el conjunto procesado de entrenamiento de 50,000 muestras. No se atribuye una causa no confirmada a la diferencia respecto al conteo nominal del ensayo.
- RMSE utiliza N como número efectivo de muestras válidas, en lugar de 300,000.
- Tablas de latencia distinguen recopilación a 100 Hz y control interno a 500 Hz; se conserva el resto de las cifras para revisión individual posterior.
- La figura de distribución sintética que rotulaba 300,000 observaciones se sustituyó en el documento por un esquema de las tres tasas. Sus archivos originales permanecen disponibles.
- Se retiran dictámenes de jitter y pérdidas asociados a los extractos incorrectos hasta disponer de sus registros originales.

Verificación: búsqueda de menciones anteriores y revisión del diff; `git diff --check` sin errores de espacios. No se modificó el software de control ni el pipeline de entrenamiento.

Compilación: el editor integrado devolvió `compile-failed` con `Unable to find standard directories for platform`. No se generó un PDF actualizado; el PDF existente corresponde a la versión previa. El archivo LaTeX se conserva para continuar las correcciones.

## 2. RF-01 no alcanzado y referencia de desempeño para TT2

Decisión del autor: conservar el requisito original de precisión y declarar que no se alcanzó en TT1. Los resultados sirven como referencia de desempeño y objetivo de mejora para TT2.

- Se explicita RMSE como métrica de evaluación de RF-01, con el umbral original menor a 0.05 rad.
- La matriz global reporta los tres valores: 0.063 rad (analítico), 0.092 rad (FP32) y 0.138 rad (INT8), con dictamen «No alcanzado».
- La verificación del módulo M2 conserva ese mismo criterio; se retira la aprobación basada en un umbral alternativo de 0.100 rad.
- Resumen, Abstract, alcance, análisis y conclusiones declaran la limitación y la referencia de desempeño.
- Se elimina la afirmación de cumplimiento de la totalidad de metas y el uso de una envolvente funcional como sustituto de RF-01.
- La recomendación de QAT establece la mejora y evaluación del criterio original en TT2, sin prometer RMSE, tamaño o latencia futuros.

Las cifras experimentales existentes se conservan para la revisión de los siguientes puntos. No se modificó el software.

## 3. Compilación y traslado a Ubuntu

Se actualizó el PDF existente mediante MiKTeX 25.12 y latexmk 4.88 en Windows, con autorización del autor. Se incorporaron rutas relativas directas a los recursos compartidos de Protocolo, sin modificar los enlaces simbólicos registrados en Git. Estas rutas son compatibles con Ubuntu.

Verificación: compilación completada con código de salida 0; PDF de 98 páginas; sin citas ni referencias cruzadas pendientes. Se revisaron visualmente las páginas de frecuencias, matriz RF-01 y conclusiones. Persisten advertencias tipográficas del reporte que no impiden compilar. El compilador integrado de Codex continúa fallando por un problema de su entorno; no se considera reparado.

El respaldo previo del PDF y las imágenes de revisión en `tmp/` son archivos locales y no se incluyen en el push. Para continuar en Ubuntu debe clonarse la rama `analyze_current_project`, que conserva el documento, el PDF y esta bitácora.

## 4. Verificación de compilación en Ubuntu

Se compiló el documento en Ubuntu con TeX Live 2023 y latexmk 4.83. Comando ejecutado desde `Documentacion/TT1/`: `latexmk -pdf -interaction=nonstopmode -halt-on-error TT1.tex`. Desde la raíz del repositorio puede emplearse `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error Documentacion/TT1/TT1.tex`; `-cd` conserva la resolución de las rutas relativas respecto al directorio del documento.

Resultado: código de salida 0 y actualización de `Documentacion/TT1/TT1.pdf` (98 páginas). BibTeX encontró los recursos compartidos de Protocolo; el registro final no contiene citas ni referencias cruzadas indefinidas. Persisten advertencias de maquetación, fuentes sustituidas y marcadores de hyperref que no impiden generar el PDF. Se revisaron visualmente la introducción a requerimientos y su tabla.

La fila RF-03 no provoca un error de compilación. No se modificó `TT1.tex` ni el software; sigue pendiente la aclaración del autor sobre torque total frente a compensación residual. Esta verificación corresponde al compilador de terminal y no confirma el funcionamiento del compilador integrado de Codex.

Se reprodujo posteriormente el fallo del compilador integrado mediante `compile_latex_document`: Tectonic activa su interfaz «version 2» y termina con un panic en `src/config.rs:154:18` porque su bundle no está en caché y falla la descarga de `https://relay.fullyjustified.net/default_bundle_v33.tar.index.gz`. El diagnóstico disponible no identifica la causa concreta de conectividad. No es un error de sintaxis de RF-03; no se modificó el documento para intentar resolverlo. La compilación local con latexmk/TeX Live continúa siendo la alternativa verificada para mantener el PDF actualizado. El fallo del compilador integrado queda pendiente de resolver en su entorno, cuya caché y conectividad no están expuestas por esta herramienta.

## 5. Arquitectura confirmada: predicción de torque total (D03)

El autor confirmó que los ensayos utilizaron la arquitectura de torque total encontrada en el código del repositorio. El controlador maestro genera `tau_cmd = tau_rnea + Kp*e + Kd*de`; el entrenamiento utiliza `tau_cmd` como objetivo y `tau_rnea` entre las 42 características. El controlador neuronal conserva el cálculo RNEA, desnormaliza la salida de la red, la satura y la aplica directamente. No suma nuevamente RNEA ni un término PD externo a la salida.

Correcciones aplicadas exclusivamente al reporte:

- Resumen y Abstract describen aprendizaje supervisado del torque total, sin atribuir identificación de fricción ni dinámica residual a esas etiquetas.
- RF-03 se precisa como predicción del torque total con RNEA como entrada, dejando explícita la corrección de la descripción previa. No se modifica retroactivamente el protocolo aprobado.
- Se incorporan las ecuaciones del objetivo maestro y de la aplicación de la salida neuronal saturada, con definición de variables.
- Arquitectura funcional, propuesta seleccionada, validación conceptual, detalle M3, comparación de controladores y conclusiones se alinean con ese contrato. Se corrige la descripción de la línea base como RNEA con PD.
- El diagrama compartido que mostraba un sumador RNEA + residual se sustituye dentro de TT1 por un esquema de señales escrito en LaTeX; el recurso original de Protocolo se conserva. Las referencias de arquitectura e integración apuntan al esquema corregido.
- Se incorpora RF-03 a la matriz global con dictamen «Implementado», sin atribuir una verificación experimental de compensación residual.
- Se distingue la latencia aislada de inferencia del cronometraje RNEA con PD y del ciclo completo. Se retira la inferencia de que el tiempo aislado de la red demuestra reemplazo o ahorro equivalente de RNEA. Las cifras restantes de latencia siguen pendientes de revisión individual.

Verificación: `git diff --check` sin errores; latexmk/pdflatex finaliza con código 0 y actualiza `TT1.pdf` a 99 páginas, sin citas ni referencias cruzadas pendientes. Revisión visual de RF-03, esquema funcional, ecuaciones del contrato, matriz de verificación y conclusiones. Persisten las advertencias tipográficas generales ya identificadas. Se mantienen las frecuencias y el dictamen de RF-01 corregidos previamente. No se modifican RNEA, límites de torque, modelos ni pipeline ML.

## 6. Integración del diagrama funcional corregido

Se revisó la segunda versión de `diagrama_funcional_torque_total.png` proporcionada por el autor. Representa RNEA como entrada neuronal, predicción del torque total, desnormalización, saturación y aplicación al robot virtual; conserva las tasas nominales de 500 Hz para control y 100 Hz para referencias y datos. Se corrigieron el tópico de referencias, la nota de generación de etiquetas durante la operación del maestro y las afirmaciones de determinismo, inmunidad al ruido y telemetría asíncrona de la primera versión.

Se reemplazó el esquema tabular provisional de TT1 por la imagen, en una página horizontal para facilitar su lectura. Se conservaron las etiquetas de arquitectura e integración y se ajustó el pie de figura. La descripción textual del servicio de publicación se alineó con el código: publicación desde `update()` y uso de `RealtimeBuffer` para recibir referencias. El archivo aparece en Git bajo `Documentacion/Protocolo/Imagenes/`, porque `Documentacion/TT1/Imagenes` es un enlace simbólico a esa carpeta compartida; el diagrama anterior permanece intacto.

Verificación: compilación con latexmk/pdflatex, código 0, PDF actualizado de 99 páginas. Revisión visual del diagrama integrado en la página física 43 (página numerada 31), sin recortes ni solapamientos; referencias de figura resueltas. Se mantiene pendiente la revisión individual de los demás hallazgos del análisis.

## 7. Motor físico y paso de integración no verificados (D04)

El autor indicó que ejecutó la simulación siguiendo las guías de Universal Robots, sin modificar la configuración del motor físico. No confirmó el motor efectivo ni el paso de integración y solicitó omitir su atribución. La configuración predeterminada de Gazebo no se toma como evidencia de la campaña concreta.

Se retiraron de TT1 las atribuciones contradictorias a DART y ODE en implementación y resultados, así como la enumeración ODE/Dart en recursos. Se eliminó el paso de integración de 1 ms (1000 Hz), cuya procedencia no está verificada, y la garantía de sincronismo asociada. Se mantiene Gazebo Harmonic con `gz_ros2_control` y el lazo interno nominal de 500 Hz, distinguiendo este periodo de control del paso de integración numérica. No se modificó la simulación ni el software.

Verificación: compilación latexmk/pdflatex completada con código 0, PDF actualizado de 99 páginas, sin citas ni referencias cruzadas pendientes; `git diff --check` sin errores. Revisión visual de las páginas físicas 60 y 77, correspondientes a implementación y entorno de pruebas. El nombre del motor y el paso efectivo de integración quedan como datos por recuperar para reproducibilidad, no como configuraciones confirmadas.

## 8. Planteamiento de latencia y margen temporal (D05)

Se corrigió la atribución de 31.8 µs a la media del controlador completo: ese valor se conserva como P95 de inferencia INT8; la media de inferencia reportada es 29.2 µs. El alcance ahora distingue estas cifras del presupuesto total medio reportado de 215.4 µs.

La tabla M3 identifica el 1.46% como fracción del periodo de 2 ms ocupada por la inferencia aislada. Se retira el dictamen «98.54% de holgura»: ese complemento no considera RNEA ni el resto de las tareas y no es el tiempo libre del ciclo completo. El margen del 89.23% se relaciona exclusivamente con el presupuesto total reportado de 215.4 µs. Se corrigen las afirmaciones de certificación o garantía temporal asociadas y la comparación que equiparaba el cronometraje RNEA con PD a la inferencia sola.

Se conservan las cifras existentes como reportadas, sin inventar mediciones nuevas ni resolver por esta corrección los hallazgos posteriores sobre procedencia del presupuesto, máximos o percentiles FP32. No se modifica el software.

Verificación: latexmk/pdflatex finaliza con código 0, PDF actualizado de 99 páginas, sin citas ni referencias cruzadas pendientes; `git diff --check` sin errores. Se revisaron visualmente las páginas físicas 20, 57, 71 y 72, que contienen el alcance, la interpretación del presupuesto y la tabla M3 con su explicación.

## 9. Jitter del periodo pendiente de verificación (D06)

El autor indicó que no dispone de contexto suficiente sobre la medición del jitter durante el proyecto y aceptó conservarlo como requisito pendiente de evaluar. Las cifras incompatibles de 0.08 ms y 0.018 ms ya se habían retirado en la corrección de frecuencias; no se sustituyen por un valor nuevo.

Se define el intervalo entre inicios de actualizaciones como `T_k = t_k - t_(k-1)` y su desviación respecto al periodo nominal como `j_k = T_k - T_s`. Se distingue esa variación de la dispersión de duración de cómputo o inferencia. La medición requiere una serie trazable del lazo interno y una referencia de reloj identificada; registrar señales a 100 Hz no verifica cada actualización interna a 500 Hz.

El umbral original de 100 µs se precisa como máximo absoluto de la desviación del periodo sobre la serie evaluada, sin presentarlo como condición universal de estabilidad. RNF-02, la tabla M1 y la matriz global conservan su evaluación temporal como «Por verificar». Se retira la afirmación de que las políticas del sistema operativo eliminan el jitter y se ajusta el encabezado del análisis de inferencia para identificarlo como dispersión del tiempo de cómputo. No se modifica el software ni se atribuye un resultado experimental nuevo.

Verificación: compilación latexmk/pdflatex con código 0, PDF actualizado de 99 páginas, sin citas ni referencias cruzadas pendientes; `git diff --check` sin errores. Revisión visual de las páginas físicas 31, 41 y 84: definición del jitter, RNF-02 y matriz global, sin recortes ni solapamientos en los cambios.

## 10. Garantías no demostradas y alcance de las conclusiones

El autor solicitó identificar información prescindible y evitar garantías sin evidencia que dificulten la defensa. Se revisaron resumen, fundamentos, selección, implementación, validación y conclusiones. Se conservan los requisitos como objetivos y las propiedades matemáticas bajo sus supuestos; no se equiparan a resultados demostrados del sistema.

- Se retiran atribuciones de determinismo, ausencia de incumplimientos temporales y estabilidad formal a partir de latencias observadas. Los tiempos en CPU/OS y el presupuesto total permanecen como reportados, con procedencia pendiente de cotejo.
- Se reconoce que el código disponible usa contenedores dinámicos durante el ciclo: la meta de ausencia de asignaciones se clasifica como «No alcanzado». No se modifica la implementación.
- Se distingue la saturación neuronal de salidas finitas de una política completa de seguridad. No se encontró comprobación explícita de finitud ni conmutación a amortiguamiento pasivo ante NaN/Inf; esas protecciones quedan pendientes. La saturación tampoco acredita límites físicos por articulación ni protección ante colisiones.
- Se retiran garantías de transferencia directa al robot físico, equivalencia de interfaces y resultados futuros de FPGA sin medición. La transferencia física se clasifica como «Pendiente TT2».
- Se elimina la atribución de eficiencia energética medida, residencia en caché y kernels específicos sin instrumentación. Se conservan tamaño de archivo y tiempos de inferencia como indicadores de software.
- Se reformulan las explicaciones del error de seguimiento como hipótesis, sin presentar causalidad ni inmunidad al ruido por fijar la aceleración a cero. Se corrige la afirmación de que z-score convierte datos arbitrarios en normales.
- Se retiran afirmaciones generales de catástrofe por cualquier retardo y de un periodo de 2 ms como exigencia universal de CTC. Se mantiene la configuración nominal del proyecto.

No se modificaron RNEA, límites de torque, pipeline ML ni configuración de ejecución. RF-01 sigue sin alcanzarse y el jitter del periodo permanece por verificar.

Verificación: latexmk/pdflatex finaliza con código 0 y actualiza TT1.pdf a 100 páginas, sin citas ni referencias cruzadas pendientes. Se revisan visualmente la matriz global y el apartado de protecciones. Se mantienen advertencias tipográficas generales del documento; git diff --check no presenta errores.

## 11. Comparación entre control analítico e inferencia aislada

El autor aclaró que la observación corresponde a los 151.2 µs, no al valor puntual de 152 µs del listing. Se conserva 151.2 µs como media reportada del módulo analítico RNEA + PD y 29.2 µs como media de inferencia INT8. Se incorpora el cociente aproximado de 19.3%, identificando que compara intervalos de distinto alcance y no acredita aceleración del controlador neuronal completo.

Se corrigen las atribuciones a RNEA aislado en selección y tablas. En el presupuesto neuronal, su duración se deja «Por medir». Al haberse utilizado 151.2 µs como componente aislado, se retiran los totales derivados de 215.4/299.7 µs y sus márgenes de las tablas, resumen, alcance y conclusiones; quedan pendientes de medición independiente. Se retira de TT1 la figura timing_budget_500hz basada en ese desglose; el archivo compartido se conserva. El rango previo de 35–48 µs no se reintroduce como resultado verificado sin registros.

Los extractos de consola se conservan y se precisa su alcance: no reconstruyen por sí solos las estadísticas de la campaña. No se modifica software ni se resuelve en esta corrección la discrepancia de percentiles FP32 (D07).

Verificación: latexmk/pdflatex finaliza con código 0 y actualiza TT1.pdf a 97 páginas, sin referencias o citas pendientes. Revisión visual de la comparación y tabla temporal en las páginas físicas 80 y 81; git diff --check sin errores. Persisten advertencias tipográficas generales ajenas a esta corrección.

## 12. Conteo de parámetros entrenables (D08, parte de arquitectura)

El autor confirmó que la latencia analítica siempre se midió con RNEA integrado al PD; no existe una medición separada que justifique el rango atribuido a RNEA aislado. Se mantiene la corrección del punto anterior.

Se corrige el conteo de 307,718 a exactamente 307,590 parámetros para la topología 42–256–512–256–128–6 de train_pytorch.py. Las cinco capas Linear incluyen sesgo: sus totales son 11,008; 131,584; 131,328; 32,896 y 774. La suma comprende 306,432 pesos y 1,158 sesgos. ReLU y Dropout no aportan parámetros entrenables. Se añade una ecuación de conteo con definición de dimensiones.

Se distingue el conteo de parámetros del tamaño serializado de ONNX y se evita asumir que todos sus tensores se almacenan en INT8. Los tamaños y porcentajes existentes permanecen como reportados, pendientes del cotejo de bytes, unidades y versión del artefacto en la siguiente revisión. No se modifican modelos ni código.

Verificación: suma independiente por capa coherente con las declaraciones Linear del script; git diff --check sin errores. Compilación latexmk/pdflatex con código 0, PDF actualizado de 97 páginas y referencias resueltas. Revisión visual de la ecuación y el conteo corregido en las páginas físicas 53 y 82.

## 13. Tamaños de modelo confirmados por el autor (D08, almacenamiento)

El autor confirmó los tamaños reales utilizados en la campaña: 1232 KB para FP32 y 315 KB para INT8. Se conservan esos valores y su unidad reportada, sin sustituirlos por las cifras de los artefactos presentes en la copia actual del repositorio. Se unifican las apariciones del reporte y se retiran los decimales adicionales 1232.40/315.18 y las conversiones inconsistentes a MB.

La reducción calculada es 100 × (1 − 315/1232) = 74.4318%, que redondea a 74.43%. Se añade la ecuación y se precisa que corresponde al tamaño del archivo ONNX, no a memoria total de inferencia, tráfico del bus o número de parámetros. No se infiere una convención KB/KiB ni un número exacto de bytes a partir de los valores confirmados. La identificación mediante hash de los archivos originales de campaña sigue siendo una tarea de trazabilidad; no se alteran los modelos.

Verificación: latexmk/pdflatex completado con código 0, PDF actualizado de 97 páginas, sin citas o referencias pendientes. Revisión visual del apartado de compresión y su ecuación en la página física 82; git diff --check sin errores.

## 14. Límite uniforme de torque como simplificación provisional

El autor explicó que el límite uniforme se adoptó por facilidad y rapidez de integración, para explorar inicialmente el comportamiento del sistema completo. Se documenta ±55 N·m como saturación provisional del controlador neuronal en simulación; la identificación y aplicación de límites por articulación se contemplan para la implementación física en TT2.

Se ajustan RF-05, la descripción del servicio, las tablas, el apartado de protecciones y las conclusiones para evitar presentar ese valor como límite físico validado universal. Se retira la atribución numérica sin verificación en la introducción. Se elimina del listing analítico una saturación ilustrativa que no aparece en el controlador disponible, manteniendo coherencia con la limitación ya registrada. No se modifica código, configuración ni valores efectivos del controlador.

Verificación: latexmk/pdflatex finaliza con código 0, PDF actualizado de 97 páginas y referencias resueltas. Revisión visual de RF-05 y justificación de la saturación provisional en las páginas físicas 40 y 76; git diff --check sin errores.

## 15. Revisión adicional de afirmaciones fuertes (observación 11)

La revisión anterior no había agotado todas las afirmaciones; ante el listado aportado por el autor se realizó una búsqueda transversal de garantías, causalidad, seguridad, robustez y superlativos. Se corrigieron afirmaciones remanentes de estabilidad numérica total, permanencia en caché, SIMD ejecutado, distribución óptima de niveles, eliminación de armónicos y daño físico por diferenciación, así como la explicación causal del RMSE por aceleración omitida. Las métricas confirmadas de inferencia, tamaños y conteo se conservan; su interpretación se limita a las condiciones evaluadas.

Se distingue la frecuencia nominal configurada en controller_manager del cumplimiento temporal. Se consultó la documentación oficial para Jazzy, además del enlace Rolling aportado por el autor: https://control.ros.org/jazzy/doc/ros2_control/controller_manager/doc/userdoc.html . Esta documentación define update_rate como frecuencia del ciclo de lectura/actualización/escritura; no se emplea para certificar la ejecución del proyecto.

Se mantienen las propiedades matemáticas de la interpolación quíntica y las definiciones de cuantización bajo sus condiciones, y los nombres de métodos de control robusto en teoría o propuestas, sin atribuir robustez experimental al sistema. Se omiten porcentajes e intervalos ilustrativos de distribución de pesos sin histograma identificado. No se modifica código, modelos ni protocolo aprobado.

Verificación: compilación latexmk/pdflatex con código 0, PDF actualizado de 96 páginas y referencias resueltas. Revisión visual de tiempo real, validación M3/trayectorias y comparación de inferencia en páginas físicas 30, 56 y 79. git diff --check sin errores; permanecen advertencias tipográficas generales del documento.

## 16. Mejora de inferencia sin atribución a SIMD (observación 12)

Se adopta la formulación solicitada: «La cuantización INT8 redujo el costo de inferencia observado bajo la configuración experimental empleada», precisando que corresponde a latencia media (37.1 → 29.2 µs, reducción del 21.29%). Se elimina en conclusiones la atribución a aritmética entera optimizada y al tránsito de parámetros como causas medidas. La mejora no se vincula a un camino SIMD sin identificar backend y kernels.

La revisión anterior ya había moderado esa atribución en los resultados y el flujo de operadores. Se ajusta además «vectorización» a «preparación» de características en las tablas, y se retira «vectorizado» del encabezado RNEA, para distinguir construcción de vectores de ejecución SIMD. El soporte AVX de la plataforma se conserva como característica de hardware, sin atribuir su uso efectivo. No se modifica la implementación ni se alteran las métricas.

Fuente consultada: https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html . La documentación describe el cálculo dinámico de escala y punto cero de activaciones; esa descripción general no identifica los kernels ejecutados en la campaña.

Verificación: latexmk/pdflatex finaliza con código 0, PDF actualizado de 96 páginas, referencias resueltas y git diff --check sin errores. Revisión visual de conclusiones en la página física 84.

## 17. Revisión integral de texto, tablas y figuras

Se revisaron visualmente las nueve imágenes utilizadas en TT1 y se contrastaron tablas, ecuaciones y configuraciones con el código. El autor confirmó utilizar la configuración del script de entrenamiento y omitir P95/P99 FP32 hasta recuperar los registros. Se unifican ReLU, Dropout 0.05 después de la segunda capa densa, 500 épocas y scheduler con paciencia 15. No se modificó el pipeline.

Se corrige la suma Pugh de A a −0.15; la de C es 1.45 y los pesos suman 1. Se diferencia CTC ideal de la ley implementada RNEA + PD en torque; se corrige el promedio MSE sobre las seis salidas estandarizadas. Se aclaran 42 entradas más 6 objetivos, los tópicos reales, la limitación de ajustar escaladores antes de dividir los datos y el alcance conceptual de las ilustraciones numéricas. RF-04 y la matriz final comparten el criterio de reducción de archivo de al menos 50%. Se retiran atribuciones de jerk continuo y de validación multiaxial con una ecuación escalar.

La articulación asociada al error estático de torque se deja por confirmar ante la discrepancia J1/hombro, sin alterar 0.038/0.046 N·m; la diferencia es +0.008 N·m. Se distingue opset solicitado por el script de versión del artefacto de campaña por cotejar. Las 50,000 filas y otras métricas sin registros trazables quedan identificadas como pendientes.

Se crea REVISION_INTEGRAL_TT1_Y_PROMPTS_GEMINI.md con prioridades y ocho prompts para conservar el estilo visual y corregir las imágenes. La figura quíntica puede conservarse como ilustración matemática. No se sobrescriben imágenes compartidas ni se integra una versión aún no generada y revisada. La distribución antigua de latencias, generada con datos aleatorios y ya excluida del reporte, no debe reincorporarse como evidencia experimental.

Verificación: compilación con latexmk/pdflatex completada correctamente, PDF de 97 páginas y referencias resueltas. Revisión visual de tablas Pugh, cuantización, latencias, dataset y matriz global; se ajusta el ancho de columnas de esta última. Persisten advertencias tipográficas generales; git diff --check sin errores. El PDF mantiene imágenes pendientes de corrección con Gemini y esta revisión no sustituye el cotejo de registros experimentales o bibliografía.

## 18. Revisión e integración de figuras corregidas — 7 de octubre de 2026

Se inspeccionan las ocho versiones suministradas por el autor. Se integran completas seis figuras: arquitectura Von Neumann, flujo RNEA, CTC teórico, PTQ/QAT, Scrum y arquitectura funcional de torque total. Se ajustan pies y explicaciones a las nuevas imágenes; se conserva la ilustración quíntica. La descripción de PTQ distingue calibración estática de cuantización dinámica aplicada en TT1. El cronometraje de 151.2 µs se mantiene atribuido a RNEA + PD integrado. Se aclaran salida estandarizada y desnormalización del torque total, frecuencia nominal y límite provisional de simulación.

La figura neuronal se integra sólo con su panel superior de topología mediante recorte de visualización en LaTeX; no se altera el PNG. Los paneles inferiores aún describen los bits del complemento a dos como campo de magnitud y requieren aclarar la fórmula FP32 para números normales y los niveles visibles del ejemplo. La figura de cuantización se omite temporalmente por título recortado y curva/escala no identificada coherentemente con el rango anunciado; se conserva su explicación matemática sin referencias huérfanas. Se añaden dos prompts específicos al informe integral para corregir estos detalles con Gemini.

Se mantiene completo el listing de inferencia para evitar que la figura se interponga entre sus líneas. No se cambia software, métricas confirmadas, protocolo ni imágenes originales.

Verificación: latexmk/pdflatex termina con código 0, PDF actualizado de 94 páginas, sin citas ni referencias cruzadas pendientes. Se revisan visualmente las siete figuras integradas y sus pies, incluido el recorte de topología y el listing completo. git diff --check sin errores; persisten advertencias tipográficas generales del documento. La integración visual pendiente se limita a los dos ajustes adicionales registrados; los pendientes de evidencia de la auditoría integral siguen vigentes.

## 19. Integración final de figuras adicionales v2 — 7 de octubre de 2026

Se revisan arquitectura_red_cuantizada_tt1_corregida_v2.png y distribucion_cuantizacion_int8_tt1_corregida_v2.png. Se integra la figura neuronal completa, eliminando el recorte temporal; se restituye la figura de cuantización y su referencia. Se ajustan explicaciones y pies para distinguir valores estandarizados de torque físico, formatos de representación de curvas didácticas, fracción FP32 de significando y rangos ilustrativos de los parámetros reales del modelo. Los ejemplos de cuantización utilizan niveles y saturaciones coherentes con sus escalas y rangos enteros.

Se mantienen las métricas confirmadas y se conservan las versiones anteriores de imágenes. No se modifica software ni el protocolo aprobado. La integración de las ocho figuras corregidas queda completada; los pendientes de evidencia experimental y bibliográfica continúan identificados en el informe integral.

Verificación: latexmk/pdflatex finaliza con código 0, PDF actualizado de 97 páginas, sin citas ni referencias cruzadas pendientes. Se inspeccionan las dos figuras completas y sus pies en las páginas físicas 55 y 68. git diff --check sin errores. Persisten advertencias tipográficas generales previamente registradas.
