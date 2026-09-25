---
name: redaccion-tt-upiita
description: >-
  Guía operativa y checklist oficial para la redacción, estructuración y verificación de los reportes de Trabajo Terminal (TT1 y TT2) en UPIITA - IPN (Ingeniería Mecatrónica). Usar siempre que se redacte, audite o revise TT1.tex o TT2.tex.
---

# Procedimiento de Redacción y Validación Oficial TT1 / TT2 (UPIITA - IPN)

Esta skill proporciona las directrices paso a paso, listas de verificación y criterios formales para escribir y validar los reportes de Trabajo Terminal de la carrera de Ingeniería Mecatrónica en UPIITA - IPN, basados en la estructura oficial de la academia de mecatrónica (`Documentacion/Normativas_y_Guias/estructura_reporte_materia_tt.md`) y la normativa institucional (`Documentacion/Normativas_y_Guias/normativa_lineamientos_upiita.md`).

---

## 1. Reglas de Estilo Inquebrantables

1. **Voz estrictamente impersonal:**
   - Redactar en tercera persona ("se calculó", "se implementó", "se observa", "se concluye").
   - Prohibido el uso de primera persona ("hicimos", "calculé", "nuestro trabajo").
2. **Rigor Matemático en LaTeX:**
   - Vectores y matrices siempre en negrita: `\bm{q}`, `\bm{\tau}`, `\bm{M}(\bm{q})`.
   - Derivadas temporales explícitas con punto o punto doble: $\dot{\bm{q}}$, $\ddot{\bm{q}}$.
   - Todas las ecuaciones deben estar numeradas dentro de entornos `\begin{equation}` y seguidas de la definición de cada una de sus variables en el texto inmediato.
3. **Calidad Tipográfica:**
   - Tablas formateadas con `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), nunca con líneas verticales toscas.
   - Figuras centradas, con etiquetas explicativas en `\caption{}` y referenciadas en el texto mediante `\ref{}`.
   - Citas bibliográficas rigurosas con `\cite{}` y sin campos faltantes en `references.bib`.
4. **Snippets de Código Clave (`listings`):**
   - Incorporar fragmentos concisos (10–25 líneas) con `\begin{lstlisting}` para ilustrar algoritmos críticos (paso RNEA en C++, bucle `update()` de `NeuralTorqueController`, o pipeline PyTorch/INT8).
   - Siempre acompañar cada snippet con una explicación técnica de su funcionamiento.
5. **Gestión y Solicitud de Imágenes:**
   - Para diagramas de bloques, marcos de referencia cinemáticos (DH del UR3e) o arquitectura de software, especificar al usuario la figura requerida y su propósito didáctico.
   - Dejar preparado en `TT1.tex` el entorno `\begin{figure}` con su respectivo `\caption` formal y etiqueta `\label{fig:...}` apuntando a `Documentacion/TT1/Imagenes/`.

---

## 2. Checklist Estructural para TT1

Antes de considerar una sección de `TT1.tex` completa, verifica los siguientes puntos:

### A. Preliminares (Numeración Romana)
- [ ] Portada institucional con datos exactos: IPN, UPIITA, Ingeniería Mecatrónica, Autor (Mendoza Díaz Ramiro), Asesor (Dr. Jorge Alejandro Juárez Lora), Profesores.
- [ ] Resumen (Español): 200–300 palabras con estructura IMRyD (Problema, Solución mecatrónica, Metodología, Resultados clave, Conclusión).
- [ ] Abstract (Inglés): Traducción técnica profesional y equivalente del Resumen.
- [ ] Palabras clave / Keywords: 4 a 6 términos técnicos normalizados.
- [ ] Nomenclatura: Tabla/glosario con definición de siglas y conceptos técnicos (RNEA, PTQ, QAT, MLP, PINN, ROS 2, ONNX, etc.).
- [ ] Simbología: Tabla rigurosa con cada variable matemática, descripción y unidades en el Sistema Internacional (SI).

### B. Inicial e Introducción (Numeración Arábiga)
- [ ] Introducción con enfoque mecatrónico explícito (Mecánica $\leftrightarrow$ Electrónica $\leftrightarrow$ Computación/IA).
- [ ] Definición del problema: Limitaciones energéticas y de cómputo en control robótico, cuello de botella de Von Neumann y carga computacional de dinámica inversa.
- [ ] Justificación: Impacto de cuantizar redes neuronales (INT8) para ejecución determinista en robótica de tiempo real.
- [ ] Objetivos: Objetivo general e individuales delimitados con claridad para TT1 y TT2.
- [ ] Antecedentes y Estado del Arte: Tabla comparativa de literatura reciente (IEEE, ScienceDirect) confrontando métodos de control, tipos de redes, cuantización y plataformas.
- [ ] Organización del documento: Breve descripción de los capítulos que componen el reporte.

### C. Capítulo 1: Marco de Referencia
- [ ] Marco Teórico: Modelado cinemático (DH modificado) y dinámico (algoritmo RNEA analítico paso a paso), redes neuronales para dinámica de robots, y teoría de cuantización (escala, zero-point, PTQ vs QAT, INT8).
- [ ] Marco Procedimental: Metodología mecatrónica (desarrollo por fases de diseño mecatrónico).

### D. Capítulo 2: Diseño del Sistema (Núcleo de TT1)
- [ ] Diseño Conceptual:
  - [ ] Necesidades y requerimientos técnicos bien tabulados (tiempos de ciclo $< 2\text{ ms}$, límites de torque $\pm 55\text{ Nm}$).
  - [ ] Arquitectura funcional (diagrama de bloques funcionales).
  - [ ] Arquitectura física en módulos mecatrónicos ($M_1$: Planta/UR3e, $M_2$: Dinámica RNEA/Control clásico, $M_3$: Red Neuronal Cuantizada e Inferencia, $M_4$: Telemetría y Adquisición).
  - [ ] Propuestas de solución alternativas por módulo y de integración global.
  - [ ] Matriz de selección de diseño conceptual (Matriz de Pugh o AHP) con justificación ponderada de la alternativa seleccionada.
- [ ] Diseño Detallado:
  - [ ] Detalle técnico de cada módulo ($M_1, M_2, M_3, M_4$): especificaciones de hardware, cinemática/dinámica, arquitectura de la red (42-256-512-256-128-6), y pipeline de despliegue.
  - [ ] Validación de cada módulo y de la integración mecatrónica global.

### E. Anexos y Administración
- [ ] Cronograma de actividades detallado.
- [ ] Presupuesto y desglose de recursos humanos, materiales y de infraestructura.
- [ ] Referencias en formato IEEE generadas limpiamente con BibTeX.
