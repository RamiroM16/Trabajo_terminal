# Análisis integral y plan de trabajo

Fecha: 6 de octubre de 2026 (America/Mexico_City).
Base revisada: commit `cda89f0`. El repositorio estaba limpio al comenzar.
Estado: diagnóstico y propuesta de ejecución; las correcciones de software, agentes y reportes todavía no se han aplicado.

## 1. Conclusión

Existe una base sustancial: reporte TT1 desarrollado, dos plugins de control ROS 2, dinámica inversa, generación de trayectorias, adquisición, entrenamiento y modelos FP32/INT8. Sin embargo, la copia disponible no permite reproducir la campaña experimental descrita. Hay discrepancias entre las instrucciones de agentes, el reporte, el código y los artefactos exportados.

La prioridad es establecer una versión experimental identificable y verificable. El pulido académico debe apoyarse en esa versión. La ausencia de registros originales en esta copia no demuestra que los experimentos no se realizaron; impide verificarlos aquí. Tampoco se ha demostrado que esta copia sea exactamente el código empleado para obtener los resultados del reporte.

## 2. Alcance de la revisión y límites

- Inventario de los 109 archivos versionados, historial reciente, configuración del IDE y enlaces simbólicos.
- Lectura de `AGENTS.md`, habilidad local de redacción y sus guías.
- Auditoría estática del paquete `ur3_custom_control`: C++, RNEA, normalización, CMake, manifiesto y plugins.
- Auditoría del pipeline Python, generadores de figuras y metadatos ONNX, sin ejecutar modelos ni deserializar pickle/checkpoints.
- Lectura de TT1, protocolo, TT2 y bibliografía compartida; contraste con el contenido compartido de ChatGPT.
- Consulta de documentación oficial de OpenAI sobre instrucciones, habilidades y subagentes.
- Extracción de los PDF normativos locales y revisión visual selectiva del esquema institucional y de una página de resultados de TT1.
- Comprobación de sintaxis de 13 scripts Python: pasan el análisis sintáctico; hay advertencias por escapes en dos cadenas de figuras. Esto no verifica sus dependencias ni resultados.

No se ejecutaron ROS 2, Gazebo, entrenamiento, inferencia ni compilación LaTeX. En esta sesión no se encontraron `ros2`, `colcon`, `cmake`, `latexmk` o `pdflatex`. No se instalaron dependencias. La revisión visual del PDF fue selectiva, no página por página. La vigencia actual de los lineamientos institucionales no se certificó; se revisaron las copias locales.

## 3. Mapa del proyecto

| Parte | Implementación disponible | Estado observado |
| --- | --- | --- |
| Protocolo | LaTeX, PDF, bibliografía y figuras compartidas | Plantea comparación energética y recursos en FPGA; mantiene FP12, INT6 y CoppeliaSim |
| TT1 | LaTeX extenso, PDF de 97 páginas y portada | Describe simulación UR3e/ROS 2/Gazebo y comparación FP32/INT8; contiene resultados cuya fuente debe recuperarse |
| TT2 | LaTeX y PDF | Plantilla parcial con secciones vacías y planteamiento anterior |
| M1, planta | Referencias documentales a UR3e/Gazebo | No hay launch, mundo, URDF ni YAML de control en el árbol revisado |
| M2, dinámica/control | `ur3e_dynamics.hpp`, `ur3_custom_controller.cpp` | Dinámica aproximada y feedforward RNEA con PD aditivo; requiere validación independiente |
| M3, red | Entrenamiento, ONNX, cuantización y controlador C++ | Modelos presentes; runtime fija FP32; exportación y evaluación necesitan revisión |
| M4, datos | Generadores, MCAP a CSV, Savitzky–Golay | No están disponibles bags, CSV ni registros completos de ensayos |
| Agentes | `AGENTS.md` y una habilidad local | Roles descritos; faltan definiciones de agentes personalizados dentro del repositorio |

### Flujo implementado

1. `random_trajectory_generator.py` publica 18 referencias: posición, velocidad y aceleración deseadas.
2. El controlador analítico calcula `RNEA(q,dq,ddq_des) + Kp*e + Kd*de`.
3. Publica 42 valores cada cinco ciclos: 36 entradas registradas y seis torques totales usados como etiquetas.
4. `bag_to_csv.py` incorpora seis aceleraciones calculadas; el dataset queda con 42 entradas y seis etiquetas.
5. PyTorch entrena una red 42→256→512→256→128→6 para imitar el torque total del controlador maestro.
6. El controlador neuronal calcula RNEA como entrada de la red, introduce cero como aceleración actual, normaliza y aplica directamente la salida neuronal al robot.

Por tanto, el código actual implementa imitación del torque total con RNEA como característica. No implementa la suma final de RNEA y un residual aprendido descrita en RF-03. Cambiar a un residual sería una decisión de diseño que exige redefinir etiquetas, ley de control y evaluación.

## 4. Hallazgos de software y aprendizaje

P0: condiciona la validez de los resultados o la ejecución fiable. P1: afecta reproducibilidad, interpretación o mantenimiento. P2: mejora formal o de organización. Estas prioridades son para el trabajo del proyecto, no una clasificación de seguridad informática.

| ID | Prioridad | Evidencia local | Hallazgo e implicación |
| --- | --- | --- | --- |
| S01 | P0 | `ros2_ws/src/ur3_custom_control/src/ur3_neural_controller.cpp:40` | Se carga únicamente `ur3_neural_controller.onnx`. El archivo INT8 existe, pero esta versión no tiene selección de modelo; hay que identificar el código usado en la campaña INT8 |
| S02 | P0 | `ros2_ws/train_pytorch.py:149`, `:168`; grafos ONNX | La exportación ocurre antes de `model.eval()`. Los artefactos FP32 e INT8 incluyen `Dropout` con `training_mode=true` y ratio 0.05. Debe reexportarse y comprobarse repetibilidad en el runtime efectivo |
| S03 | P0 | `ur3e_dynamics.hpp:99`, `:115` | La recurrencia de aceleración combina la traslación expresada en el marco padre con velocidades/aceleraciones del hijo. Hay una inconsistencia de marcos y de origen; requiere contraste numérico con un solver independiente |
| S04 | P0 | `ur3e_dynamics.hpp:36` | Todas las inercias son `0.01*I`; centros de masa aproximados y carga externa omitida. No equivale a un modelo inercial completo verificado del fabricante |
| S05 | P0 | `ur3_custom_controller.cpp:125`, `:153`; `ur3_neural_controller.cpp:178` | Baseline sin saturación explícita; neuronal limita todos los pares a ±55 y permite que NaN atraviese las comparaciones. Falta política de finitud, fallos, límites por articulación y comandos vencidos |
| S06 | P0 | `ur3_custom_controller.cpp:108`; `ur3_neural_controller.cpp:157` | Temporización baseline incluye dinámica y PD; neuronal mide solo `Run`. No son medidas equivalentes del ciclo completo |
| S07 | P1 | Ambos `update()`; `ur3e_dynamics.hpp:56` | Se construyen vectores dinámicos, se copia el comando, hay publicación/logging ROS y asignaciones de salida de inferencia. Contradice la afirmación de ausencia de reservas dinámicas |
| S08 | P1 | `bag_to_csv.py:91`; `ur3_neural_controller.cpp:130` | Aceleración filtrada en entrenamiento y ceros en despliegue. La coincidencia dimensional no garantiza que las entradas representen la misma distribución |
| S09 | P1 | `train_pytorch.py:50`, `:63`; `train_full.py:43`, `:53` | Scalers ajustados antes del split: fuga de información confirmada. División aleatoria de muestras temporales también puede inflar evaluación; dividir por trayectoria/campaña |
| S10 | P1 | `train_pytorch.py:71`, `:171` | `test_loader` sin uso y evaluación final de una muestra/articulación. No hay evaluación independiente completa ni equivalencia PyTorch/ONNX/INT8 |
| S11 | P1 | `bag_to_csv.py:39`, `:91`; `random_trajectory_generator.py:40` | Timestamp del bag descartado, `dt=0.01` supuesto, trayectorias con reloj de pared y semillas no registradas. Falta medir pérdidas y preservar tiempo de simulación |
| S12 | P1 | `train_full.py:59`; `export_scalers_to_cpp.py:8` | TensorFlow y PyTorch usan topologías distintas y sobrescriben scalers con los mismos nombres. Falta manifest que vincule modelo, features y normalización |
| S13 | P1 | CMake y `package.xml` | Falta declaración de `ament_index_cpp` y de `std_msgs` en el manifiesto; C++17 no se establece expresamente; dependencia ONNX Runtime binaria de Linux |
| S14 | P1 | `ur3_custom_controller.cpp:133`; `ur3_neural_controller.cpp:190` | Log calcula RMS instantáneo entre seis articulaciones, no RMSE temporal sobre toda una trayectoria. No se pueden sustituir ambas métricas sin una definición y cálculo explícitos |
| S15 | P1 | Activación/desactivación de ambos plugins | Referencia inicial fija de tipo cobra y desactivación sin transición explícita de esfuerzos. El comportamiento final depende del administrador/hardware y requiere verificación |

El hallazgo S03 es estático. Contraejemplo para diseñar una prueba: antecesores inmóviles, posiciones cero y solamente aceleración de articulación 3 igual a uno; el origen de esa articulación no debe acelerar por su propia rotación, pero la fórmula incorpora `z×[-0.24355,0,0]`. No se ejecutó un solver para establecer el error final de torque.

También quedan por verificar la vida útil de `Ort::Env`, creada localmente durante configuración, y la compatibilidad efectiva entre el runtime 1.16.3 y los modelos. No se clasifican como fallos demostrados de ejecución.

### Artefactos observados

- Topología PyTorch/ONNX: 307,590 parámetros, no 307,718.
- Modelo FP32 raíz: 1,245,167 bytes; INT8: 322,310 bytes. Reducción aproximada: 74.11% para estos archivos concretos.
- Los hashes de modelos raíz y `config/` coinciden. `entrenamiento1/` contiene otra versión del modelo.
- El grafo actual declara opset 18 e IR 9; el script solicita opset 9. Debe registrarse el procedimiento real de exportación.
- INT8 contiene cuantización dinámica y `MatMulInteger`, pero conserva partes flotantes. La existencia de esos nodos no demuestra por sí sola el kernel SIMD ejecutado ni consumo eléctrico reducido.
- Algunos `.onnx.data` acompañan modelos que ya contienen pesos embebidos. No sumarlos ni eliminarlos sin verificar las referencias externas de cada grafo.

## 5. Documentación y evidencia experimental

| ID | Prioridad | Ubicación | Hallazgo |
| --- | --- | --- | --- |
| D01 | P0 | `generate_latency_distribution_figure.py:17` y `TT1.tex:1667` | El script genera muestras aleatorias calibradas a medias/dispersiones; TT1 presenta su histograma y ECDF como distribución empírica de 300,000 ciclos. Recuperar registros y regenerar o etiquetar explícitamente como ilustración sintética |
| D02 | P0 | `TT1.tex:810`, `:1928` | RF-01 especifica `e_q < 0.05 rad`, pero la matriz cambia a envolvente funcional y declara validación con errores mayores. Primero precisar qué métrica es `e_q`, luego evaluar el mismo criterio; si es RMSE, los valores reportados exceden 0.05 |
| D03 | P0 | `TT1.tex:812`, `:1130`, `:1589` | Requisito/narrativa residual frente a etiqueta torque total y aplicación directa de NN. Fijar la arquitectura real antes de corregir ecuaciones y diagramas |
| D04 | P1 | `TT1.tex:1327`, `:1777` | DART en implementación y ODE en resultados. Verificar configuración utilizada antes de elegir uno |
| D05 | P1 | `TT1.tex:352`, `:1838` | 31.8 µs aparece como promedio del controlador completo y también como P95 de inferencia; además se confunden holgura de inferencia y de ciclo completo |
| D06 | P1 | `TT1.tex:1345`, `:1362` | `std dev=0.00008 s` equivale a 0.08 ms, pero la tabla da jitter 0.018 ms. Definir fórmula, ventana y fuente; no sustituir números sin revisar |
| D07 | P1 | `TT1.tex:1654`, `:1837` | P95/P99 FP32 cambian entre tablas: 39.4/41.2 y 40.2/41.5. Consolidar desde una campaña identificada |
| D08 | P1 | `TT1.tex:1890`; modelos | Conteo incorrecto de parámetros y tamaños que no coinciden exactamente con la copia actual. Definir bytes, KB/KiB y hash de versión |
| D09 | P1 | `TT1.tex:1862`, `:1882` | 151.2 µs se atribuye a RNEA aunque instrumentación baseline incluye PD; presupuesto completo no tiene instrumentación por subproceso disponible en esta copia |
| D10 | P1 | `TT1.tex:1902`, `:1957` | Afirmaciones sobre caché, SIMD, ausencia de asignaciones y garantías temporales exceden la evidencia disponible; algunas contradicen el código |
| D11 | P1 | TT1 objetivos; protocolo; TT2 | Protocolo/TT2 mantienen PID, FP12, varias precisiones y FPGA; TT1 se concentra en feedforward+PD, FP32/INT8 CPU. Documentar evolución y cumplimiento por fase; no reescribir retroactivamente un protocolo aprobado |
| D12 | P1 | Capítulo 4 TT1 y anexos | No hay secciones específicas de análisis de costos/valor equivalentes al esquema institucional; presupuesto estimado en anexos no sustituye análisis de costos reales |

Hay listings de consola dentro de TT1, pero unos pocos valores no permiten reconstruir medias, percentiles, máximos, RMSE global ni una serie de 300,000 ciclos. Los efectos atribuidos a cuantización o aceleración omitida son hipótesis plausibles que necesitan ensayos de ablación para convertirse en conclusiones causales.

La bibliografía compartida tiene entradas y DOI, pero el catálogo no acredita verificación individual. La carpeta de artículos no contiene los PDF enumerados en esta copia; `.gitignore` los excluye. Algunas entradas parecen ejemplos pendientes de depurar (`smith_autonomous_2020`, `garcia_mecatronics_2019`, `roberts_robot_2015`). Su autenticidad y uso deben comprobarse, sin afirmar que sean inventadas por su nombre.

La revisión de claves citadas de TT1 contra la bibliografía real de Protocolo no encontró claves ausentes ni duplicadas. Sí hay duplicación conceptual de Spong y metadatos de autores por normalizar. Falta una tabla comparativa formal de estado del arte y un registro afirmación → página de la fuente, particularmente para porcentajes y conclusiones específicas.

Otros ajustes que deben entrar en la consolidación:

- Los máximos por subproceso de la tabla suman exactamente 299.7 µs, el valor denominado máximo observado del ciclo (`TT1.tex:1275`). La suma de máximos separados no demuestra el máximo medido de la ejecución conjunta.
- ReLU en topología (`:1151`) frente a LeakyReLU en implementación (`:1469`); 500 épocas/paciencia 15 (`:1160`) frente a 150/paciencia 10 (`:1472`). Registrar configuración efectiva.
- El texto de jitter usa también la palabra varianza con unidades de tiempo, que no corresponden a una varianza; separar dispersión de periodo y de cómputo.
- Z-score no vuelve normal una distribución arbitraria ni garantiza 99.73% dentro de ±3 desviaciones; revisar ese argumento (`:944`, `:1537`).
- La cifra 300,010 mensajes/600.02 s corresponde a aproximadamente 500 Hz y a `/joint_states`; ese registro no demuestra por sí solo disponibilidad de etiquetas y 42 features sincronizadas (`:1715`).
- El objetivo TT1 de definir al menos dos precisiones sigue vigente en el texto, pero la implementación revisada muestra sólo INT8. Registrar cuál segunda precisión se estudiará y en qué etapa.
- QAT con RMSE ≤0.06, FPGA a 1.8–3.5 µs y menos de 3 W son proyecciones (`:2005`, `:2016`), pendientes de dimensionamiento y medición.

## 6. Implementación de agentes

### Qué existe

`AGENTS.md` define un orquestador llamado Antigravity, tres especialistas y comunicaciones bidireccionales. La única habilidad local es `redaccion-tt-upiita`; su frontmatter tiene `name` y `description`. No se encontraron `.codex/config.toml`, `.codex/agents/*.toml`, definiciones locales de los especialistas ni un ejecutor `invoke_subagent`.

Esto proporciona instrucciones de colaboración, pero no registra por sí mismo tres agentes personalizados. En esta revisión se usaron tres subagentes temporales con tareas de auditoría, al amparo del protocolo de delegación de `AGENTS.md`; no se probaron los roles personalizados descritos como una configuración persistente.

La documentación oficial consultada distingue instrucciones de proyecto (`AGENTS.md`), habilidades reutilizables (`SKILL.md`) y agentes personalizados definidos en TOML. La configuración global del usuario no se auditó; la ausencia local no demuestra que no exista una configuración personal externa.

### Problemas concretos

1. Dependencias de Antigravity y rutas `file:///home/ramiro/...` en instrucciones y README. No son portables a esta sesión.
2. `invoke_subagent` se menciona como herramienta, pero no es un mecanismo definido en el repositorio ni una herramienta disponible con ese nombre en esta sesión.
3. El nombre del arquitecto difiere entre diagrama y encabezado.
4. No existen contratos de entrada/salida, propietario de archivos, revisión independiente ni reglas de integración para evitar ediciones concurrentes en TT1/bibliografía.
5. No hay comando de compilación, entorno reproducible ni criterios ejecutables de validación asociados a los roles.
6. Las instrucciones fijan ±55 N·m y la topología como hechos permanentes, lo que puede propagar valores no verificados al documento.
7. La habilidad se autodenomina checklist oficial aunque las guías Markdown mezclan esquema institucional con decisiones del proyecto: Scrum, UR3e, ±55, red y cuantización. El PDF original de estructura define capítulos, no esas elecciones técnicas.
8. El requisito anti-alucinación está bien planteado, pero falta una bitácora de verificación de bibliografía y de cifras experimentales.
9. La habilidad orienta a pedir imágenes y preparar entornos, pero falta un procedimiento que compruebe archivos, origen de datos y compilación. En esta fase sólo se aplicó a la auditoría; no se editaron reportes.

### Organización propuesta

| Rol | Responsabilidad y propiedad | Resultado exigido |
| --- | --- | --- |
| Orquestador | Plan, decisiones, integración y asignación de archivos | Backlog actualizado, dependencias, estado de verificación |
| Arquitecto robótico | Control, dinámica, seguridad e integración ROS | Código y pruebas reproducibles; evidencia de fórmulas/mediciones |
| Investigador científico | Verificación de fuentes y fundamentos | Registro de fuente, DOI/URL, afirmación respaldada y sección |
| Redactor académico | TT1/TT2 y figuras basadas en evidencia validada | Secciones coherentes, requisitos trazables y PDF compilado |
| Revisor de evidencia (tarea temporal) | Contraste independiente antes de cierre | Hallazgos con ruta/línea, campaña y criterio de aceptación |

Mantener tres especialistas persistentes sería suficiente; la revisión independiente puede asignarse temporalmente sin añadir complejidad permanente. Un mismo archivo debe tener un único editor durante cada tarea. El investigador propone entradas; el responsable de bibliografía las integra. Ningún rol debe declarar cumplido un requisito sólo por acuerdo entre agentes.

## 7. Portabilidad y reproducibilidad

Git registra enlaces simbólicos para `Imagenes`, `references.bib` y `IEEEtran.bst` en TT1/TT2, y `libonnxruntime.so`. En este checkout de Windows son archivos de texto con el destino del enlace. Por ello, una compilación convencional que dependa de esos recursos no funcionará sin resolver la estrategia de portabilidad. No se cambiaron esos archivos durante la auditoría.

Faltan README general de ejecución, versiones de dependencias Python/ROS, configuración de simulación, adquisición y reproducción de pruebas, datasets, logs completos y manifest de modelos. Esto debe resolverse con archivos pequeños versionados y un almacenamiento documentado para datos grandes. Ignorar los datos en Git puede ser apropiado; no debe implicar perder la referencia, el hash ni su ubicación de recuperación.

El entorno de referencia inferido es Ubuntu 24.04/ROS 2 Jazzy/Gazebo Harmonic, no este PowerShell de Windows. Antes de decidir WSL, contenedor o máquina Linux hay que localizar el entorno en que se obtuvieron los resultados y registrar sus versiones.

## 8. Plan por etapas y criterios de cierre

| Etapa | Trabajo | Entregable | Criterio de cierre | Dependencia |
| --- | --- | --- | --- | --- |
| 0. Preservar y reconstruir procedencia | Catalogar código, modelos y campañas; localizar bags, logs, launch/YAML/URDF y scripts usados | Inventario con hashes y matriz de evidencias | Cada cifra de resultados tiene fuente o estado explícito de pendiente/no verificable | Ninguna |
| 1. Operar los agentes | Simplificar AGENTS, separar normas/decisiones, definir especialistas y contratos; verificar descubrimiento de skill | Configuración local portable y una tarea de prueba por rol | Cada rol responde a su alcance, cita evidencia y respeta propiedad de archivos | Etapa 0 para no fijar métricas dudosas |
| 2. Fijar arquitectura y entorno | Decidir torque total vs residual; documentar ecuación baseline; resolver enlaces y dependencias; recuperar simulación | Contrato de señales, README y entorno reproducible | Un checkout limpio compila y carga plugins/modelos en el entorno acordado | Etapa 0 |
| 3. Validar dinámica y protecciones | Revisar RNEA, identificar inercias/CoM, contrastar solver; gestionar comandos, finitud, límites y fallos | Pruebas numéricas e integración con política de límites | Casos de gravedad, aceleración y velocidad contrastados; comandos anómalos producen respuesta definida | Etapa 2 |
| 4. Reconstruir aprendizaje | Timestamps y trayectorias, split por campaña, scalers sólo train; alinear aceleración; exportar eval; manifest y equivalencia | Dataset catalogado, modelos FP32/INT8 y evaluación completa | Repetibilidad y paridad Python/ONNX/C++; conjunto de prueba independiente y métricas por articulación | Etapas 2–3; corregir dinámica puede invalidar etiquetas anteriores |
| 5. Medir comparativamente | Modelo seleccionable, trayectorias idénticas, warmup, reloj monotónico, ciclo e inferencia separados, repeticiones y logging fuera del ciclo | Registros originales y scripts que generen tablas/figuras | RMSE temporal definido, percentiles y pérdidas/deadlines calculados de registros; cada ejecución identifica modelo/configuración | Etapas 3–4 |
| 6. Cerrar TT1 | Requisitos con criterio original, correcciones de cifras y nombres; eliminar garantías no sustentadas; figuras reales/ilustrativas identificadas; costos/valor y bibliografía | TT1 actualizado y compilado con revisión visual | Tabla de cumplimiento trazable, referencias resueltas y coherencia código–documento–datos | Etapa 5 para afirmaciones experimentales; correcciones formales pueden avanzar antes |
| 7. Delimitar TT2 | Relacionar protocolo y avances; definir QAT, medición energética, plataforma y acceso físico reales | Plan TT2 medible y compatible con compromisos académicos | Recursos, interfaz real y experimentos factibles identificados; predicciones separadas de resultados | Arquitectura validada y decisiones de alcance |

Las etapas 1 y 2 pueden avanzar parcialmente en paralelo. Las correcciones editoriales independientes también. El orden de generación de datos sí depende de la dinámica y de la arquitectura: entrenar nuevamente antes de resolverlas podría producir otro conjunto de etiquetas que haya que reemplazar.

### Primer bloque de ejecución recomendado

- [ ] Registrar los artefactos actuales y su procedencia sin sobrescribirlos.
- [ ] Recuperar el entorno y registros que produjeron la comparación INT8.
- [ ] Crear matriz requisito → prueba → registro → cálculo → tabla/figura.
- [ ] Acordar la arquitectura que realmente se va a reportar y medir.
- [ ] Preparar configuración de agentes con roles, límites de edición y resultados verificables.

### Criterios comunes para declarar una tarea terminada

- La afirmación o modificación está vinculada a un archivo/versionado y a una prueba pertinente.
- Los resultados distinguen observación, cálculo, hipótesis y predicción.
- Una segunda revisión comprueba consistencia entre código, experimento y reporte.
- Modelos/datasets nuevos no reemplazan silenciosamente los anteriores.
- El estado de los requisitos conserva el criterio original; cualquier cambio queda justificado y registrado.

## 9. Decisiones que deben resolverse durante la ejecución

1. ¿La copia revisada es la versión experimental final o faltan cambios de la máquina Linux?
2. ¿Dónde están bags, CSV, latencias completas, configuraciones de simulación y trayectorias originales?
3. ¿La contribución será imitación de torque total o compensación residual? La evidencia actual corresponde a la primera.
4. ¿Qué expresa RF-01 exactamente: error instantáneo, máximo, RMSE temporal por articulación o global?
5. ¿Qué interfaz de control y recursos estarán realmente disponibles en TT2? La interfaz de esfuerzo simulada no prueba por sí sola acceso equivalente en el robot físico.
6. ¿Cuál es la fecha de entrega/defensa y qué recursos de hardware están confirmados? El plan actual establece dependencias, no fechas ni duraciones inventadas.

## 10. Fuentes para la configuración de agentes

Consultadas el 6 de octubre de 2026:

- [Instrucciones de proyecto AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- [Subagentes y definiciones personalizadas](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- [Habilidades reutilizables](https://learn.chatgpt.com/docs/build-skills).

Las copias originales locales de `Documentacion/Normativas_y_Guias/Estructura_TT.pdf` y `Lineamientos_TT.pdf` se contrastaron con las guías Markdown. La distinción entre estructura institucional y decisiones técnicas del proyecto debe conservarse al actualizar la habilidad.
