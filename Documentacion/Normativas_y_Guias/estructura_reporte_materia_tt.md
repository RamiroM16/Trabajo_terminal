# Estructura Oficial del Reporte Escrito de Trabajo Terminal (TT1 y TT2)
**Carrera:** Ingeniería en Mecatrónica  
**Institución:** Unidad Profesional Interdisciplinaria en Ingeniería y Tecnologías Avanzadas (UPIITA - IPN)  
**Fuente Oficial:** Aprobado en la reunión de la Academia de Mecatrónica de UPIITA – IPN. Basado en el marco metodológico del libro *"Redacción Técnica"* de Rosalía Díaz-Barriga Martínez (Ediciones IPN).

---

## 1. Diagrama General de la Estructura

El reporte escrito se divide en cinco partes fundamentales:

```text
+-----------------------------------------------------------------------------------+
| 1. PARTE PRELIMINAR (Páginas con numeración romana: i, ii, iii...)               |
|    - Portada oficial institucional (IPN / UPIITA)                                 |
|    - Portada con firmas de aprobación (Asesor y Profesores)                      |
|    - Dedicatoria (opcional)                                                       |
|    - Agradecimientos (opcional)                                                   |
|    - Contenido (Índice general)                                                   |
|    - Resumen (Español)                                                            |
|    - Abstract (Inglés)                                                            |
|    - Índice de figuras                                                            |
|    - Índice de tablas                                                             |
|    - Nomenclatura (Glosario formal de términos y conceptos técnicos)              |
|    - Simbología (Definición exhaustiva de variables, vectores y matrices)        |
+-----------------------------------------------------------------------------------+
| 2. PARTE INICIAL (Comienza numeración arábiga: 1, 2, 3...)                        |
|    - Introducción                                                                 |
|      * Enfoque mecatrónico                                                        |
|      * Definición del problema                                                    |
|      * Justificación                                                              |
|      * Objetivo (General y Específicos para TT1 y TT2)                            |
|      * Antecedentes                                                               |
|      * Organización del documento                                                 |
+-----------------------------------------------------------------------------------+
| 3. PARTE MEDIA (Cuerpo técnico del proyecto - Capítulos 1 al 4)                   |
|                                                                                   |
|    Capítulo 1: Marco de Referencia                                                |
|      1.1. Marco teórico (Fundamentación matemática, robótica y ML)                |
|      1.2. Marco procedimental (Metodología de diseño mecatrónico)                 |
|                                                                                   |
|    Capítulo 2: Diseño del Sistema                                                 |
|      2.1. Diseño conceptual                                                       |
|           2.1.1. Necesidades - requerimientos                                     |
|           2.1.2. Arquitectura funcional (funciones y flujos)                     |
|           2.1.3. Arquitectura física (módulos M_1 ... M_n)                        |
|           2.1.4. Propuestas de solución                                           |
|                  2.1.4.1. Módulos (M_1 ... M_n)                                   |
|                  2.1.4.2. Integración (sistema)                                   |
|           2.1.5. Validación                                                       |
|           2.1.6. Selección de diseño conceptual (Matriz Pugh / AHP)               |
|      2.2. Diseño detallado                                                        |
|           2.2.1. Detalle módulo 1 (M_1)                                           |
|                  2.2.1.i. Validación (M_1)                                        |
|           2.2.2. Detalle módulo 2 (M_2)                                           |
|                  2.2.2.i. Validación (M_2)                                        |
|           2.2.i. Detalle módulo n (M_n)                                           |
|                  2.2.i.i. Validación (M_n)                                        |
|           2.2.i+1. Integración sistema mecatrónico                                |
|                  2.2.i+1.i. Validación sistema mecatrónico                        |
|                                                                                   |
|    Capítulo 3: Implementación del Sistema                                         |
|      3.1. Implementación módulo 1 (M_1)                                           |
|           3.1.i. Verificación (M_1)                                               |
|      3.2. Implementación módulo 2 (M_2)                                           |
|           3.2.i. Verificación (M_2)                                               |
|      3.i. Implementación módulo n (M_n)                                           |
|           3.i.i. Verificación (M_n)                                               |
|      3.i+1. Integración del sistema mecatrónico                                   |
|           3.i+1.i. Verificación del sistema mecatrónico                           |
|                                                                                   |
|    Capítulo 4: Análisis de Resultados                                             |
|      4.1. Análisis de ingeniería (Métricas de error, latencia, consumo)           |
|      4.2. Análisis de costos (Presupuesto real, componentes, horas hombre)        |
|      4.3. Análisis de valor (Relación costo/beneficio, impacto tecnológico)       |
+-----------------------------------------------------------------------------------+
| 4. PARTE FINAL                                                                    |
|    - Conclusiones                                                                 |
|    - Recomendaciones y trabajo a futuro                                           |
+-----------------------------------------------------------------------------------+
| 5. PARTE ADICIONAL                                                                |
|    - Apéndices                                                                    |
|    - Anexos (Administración del proyecto, cronograma, cartas de VoBo)             |
|    - Fuentes – Referencias (Estilo IEEE, formato BibTeX)                          |
|    - Glosario                                                                     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Especificación Detallada Sección por Sección

### 2.1. Preliminares (Numeración Romana)
* **Portada:** Título oficial registrado, logotipos de IPN y UPIITA, nombre completo del autor, asesor(es) y profesores sin abreviaturas erróneas.
* **Resumen / Abstract:** Extensión recomendada de 200 a 300 palabras. Estructura recomendada:
  1. Contexto y motivación del proyecto.
  2. Planteamiento conciso del problema.
  3. Propuesta de solución y metodología aplicada.
  4. Resultados cuantitativos clave obtenidos (o esperados en TT1).
  5. Conclusión principal o aportación.
* **Palabras clave:** De 4 a 6 palabras o descriptores estandarizados (ej., *Redes neuronales cuantizadas, Control de robots, Inferencia en tiempo real, ROS 2, Dinámica analítica*).
* **Nomenclatura:** Glosario de términos especializados, siglas y abreviaturas técnicas (ej., RNEA, PTQ, QAT, MLP, RMSE, ROS, ONNX).
* **Simbología:** Tabla rigurosa de variables matemáticas indicando su símbolo, descripción y unidades SI:
  - $\bm{q}, \dot{\bm{q}}, \ddot{\bm{q}}$: Vectores de posición, velocidad y aceleración articular ($\text{rad}$, $\text{rad/s}$, $\text{rad/s}^2$).
  - $\bm{\tau}_{cmd}, \bm{\tau}_{rnea}$: Vectores de pares/torques articulares ($\text{N}\cdot\text{m}$).
  - $K_p, K_d$: Matrices de ganancias proporcional y derivativa.

---

### 2.2. Parte Inicial (Numeración Arábiga)
* **Introducción:** Panorama global del proyecto.
* **Enfoque mecatrónico:** Justificación de la interdisciplinariedad del sistema (Mecánica: cinemática/dinámica de manipulación $\leftrightarrow$ Electrónica/Hardware: actuadores y procesamiento embebido $\leftrightarrow$ Computación/IA: algoritmos en C++ de tiempo real, ROS 2 y redes neuronales).
* **Definición del problema:** Cuello de botella computacional, consumo de recursos y limitación de las técnicas clásicas frente al cálculo dinámico y la IA.
* **Justificación:** Importancia académica, tecnológica e industrial de optimizar redes neuronales (INT8) para controlrobótico sin perder estabilidad.
* **Objetivos:**
  * **Objetivo General:** Un solo objetivo redactado en infinitivo, medible y que resuma el impacto final.
  * **Objetivos Específicos TT1:** Metas concretas para la primera fase (investigación, diseño conceptual, formulación matemática de dinámica, arquitectura de red, cuantización base y diseño experimental).
  * **Objetivos Específicos TT2:** Metas de la segunda fase (implementación en banco de pruebas/robot, entrenamiento masivo, cuantización en hardware, experimentación comparativa, análisis de resultados).
* **Antecedentes y Estado del Arte:** Evolución de las técnicas de control clásico a control inteligente, con tabla comparativa de literatura científica reciente.
* **Organización del documento:** Breve párrafo descriptor de lo que el lector encontrará en cada capítulo.

---

### 2.3. Capítulo 1: Marco de Referencia
* **1.1. Marco Teórico:**
  * Fundamentos de cinemática y dinámica analítica (Denavit-Hartenberg modificado, RNEA paso hacia adelante y hacia atrás, formulación de Lagrange-Euler).
  * Redes neuronales artificiales para regresión y dinámica inversa (MLP, PINNs).
  * Teoría de compresión y cuantización de redes (escala y punto cero, cuantización simétrica/asimétrica, PTQ vs QAT, INT8 vs FP32).
* **1.2. Marco Procedimental (Metodología Mecatrónica):**
  * Definición del ciclo metodológico empleado: En este proyecto se adoptó formalmente el marco de trabajo ágil **Scrum adaptado al desarrollo mecatrónico** (con Sprints, Épicos en el Product Backlog, reuniones periódicas de asesoría e incrementos evaluables).

---

### 2.4. Capítulo 2: Diseño del Sistema
Esta es la sección central evaluada en **TT1**.
* **2.1. Diseño Conceptual:**
  * **2.1.1. Necesidades - requerimientos:** Tabla de requerimientos funcionales y no funcionales (tiempos de ciclo $< 2\text{ ms}$, límites de torque $\pm 55\text{ Nm}$, precisión de seguimiento, peso del modelo).
  * **2.1.2. Arquitectura funcional:** Diagrama funcional de cajas negras y flujos de materia, energía e información.
  * **2.1.3. Arquitectura física (módulos):** Descomposición del sistema mecatrónico en módulos:
    * $M_1$: Planta Robótica y Simulación (UR3e, dinámica física, Gazebo/ros2_control).
    * $M_2$: Módulo de Control Dinámico y Algoritmos (RNEA analítico + PD).
    * $M_3$: Módulo de Inteligencia Artificial y Cuantización (PyTorch, ONNX, motor INT8 ONNX Runtime).
    * $M_4$: Módulo de Supervisión, Adquisición y Telemetría (Rosbags, filtrado Savitzky-Golay, generación de trayectorias).
  * **2.1.4. Propuestas de solución:** Al menos 2 o 3 alternativas viables por cada módulo y para la integración global.
  * **2.1.5. Validación conceptual:** Criterios teóricos para descartar opciones no viables.
  * **2.1.6. Selección del diseño conceptual:** Matriz de selección estructurada (Matriz de Pugh o Proceso de Jerarquía Analítica - AHP) con criterios ponderados y justificación de la alternativa ganadora.
* **2.2. Diseño Detallado:**
  * Detalle ingenieril a fondo de cada módulo seleccionado ($M_1, M_2, M_3, \dots$): ecuaciones de dimensionamiento, diagramas de clases, interfaces de comunicación, esquemas de flujo.
  * *Validación de cada módulo:* Demostración analítica o mediante simulación de que el diseño cumplirá con los requerimientos.
  * *Integración y validación del sistema mecatrónico:* Diagrama de integración global de señales, buses, tópicos de ROS 2 y acoplamiento temporal.

---

### 2.5. Capítulo 3: Implementación del Sistema (Foco TT2 / Avances TT1)
* **Diferencia entre Validación y Verificación:**
  * **Validación (en Diseño):** Demuestra que el *diseño* teórico resuelve la necesidad planteada (*"¿Diseñamos el sistema correcto?"*).
  * **Verificación (en Implementación):** Pruebas de funcionamiento real con datos y mediciones para comprobar que la construcción cumple las especificaciones (*"¿Construimos el sistema correctamente?"*).
* Documenta la implementación paso a paso de cada módulo ($M_1 \dots M_n$), bancos de pruebas, código desarrollado y su verificación experimental individual y de conjunto.

---

### 2.6. Capítulo 4: Análisis de Resultados
* **4.1. Análisis de Ingeniería:** Comparativas cuantitativas:
  * Gráficas de seguimiento articular $q(t)$ vs $q_{des}(t)$.
  * RMSE (Root Mean Square Error) por articulación y global.
  * Latencias de inferencia ($\mu\text{s}$) y jitter temporal.
  * Reducción de memoria (FP32 vs INT8).
* **4.2. Análisis de Costos:** Desglose económico exhaustivo: licencias de software, equipo de cómputo, robot manipulador, consumibles, horas-hombre de desarrollo e ingeniería.
* **4.3. Análisis de Valor:** Relación costo-beneficio, eficiencia energética estimada y valor agregado del control inteligente cuantizado frente al control convencional.

---

### 2.7. Final y Adicionales
* **Conclusiones:** Conclusiones puntuales orientadas a responder el cumplimiento de cada uno de los objetivos específicos y general.
* **Recomendaciones y Trabajo Futuro:** Líneas abiertas para TT2 o investigaciones posteriores.
* **Anexos y Apéndices:** Cronograma de Gantt, constancias de protocolo, hojas técnicas del robot.
* **Referencias:** Bibliografía completa en formato IEEE.
