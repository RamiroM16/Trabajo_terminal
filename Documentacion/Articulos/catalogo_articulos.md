# Catálogo y Mapeo Maestro de Literatura Técnica y Científica
**Ubicación:** `Documentacion/Articulos/`  
**Destino:** Sustento teórico, metodológico y bibliográfico de `Documentacion/TT1/TT1.tex` y `TT2.tex`

---

## 1. Libros Canónicos de Fundamentos de Robótica y Control

| Archivo PDF | Clave BibTeX | Título / Autores | Temas Clave / Capítulos de Impacto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `Spong-RobotmodelingandControl.pdf` | `@book{Spong}` / `@book{spong2006robot}` | *Robot Modeling and Control*<br>M. Spong, S. Hutchinson, M. Vidyasagar | - Cinemática directa/inversa (DH)<br>- Dinámica de manipuladores (Euler-Lagrange y Newton-Euler)<br>- Control por par computado (*Computed Torque Control*) | **Capítulo 1:** Marco Teórico (1.1)<br>**Capítulo 2:** Diseño Detallado Módulo $ (RNEA) |
| `MR.pdf` | `@book{modern_robotics}` | *Modern Robotics: Mechanics, Planning, and Control*<br>K. Lynch, F. Park (Cambridge Univ. Press) | - Algoritmo Recursivo Newton-Euler (RNEA)<br>- Cinemática en espacio articular y operacional<br>- Propiedades de la matriz de inercia y Coriolis | **Capítulo 1:** Marco Teórico (1.1)<br>**Capítulo 2:** Detalle de dinámica analítica |
| `fundamentos-de-robotica.pdf` | *(Por citar)* | *Fundamentos de Robótica*<br>A. Barrientos, L. Peñín, C. Balaguer, R. Aracil (McGraw-Hill) | - Parámetros Denavit-Hartenberg modificados<br>- Actuadores y sensores en robótica industrial<br>- Estructuras mecánicas de robots seriales | **Capítulo 1:** Marco Teórico<br>**Capítulo 2:** Diseño Módulo $ (UR3e) |
| `Ingenieria_de_Control_Moderna_Ogata_5ed.pdf` | *(Por citar)* | *Ingeniería de Control Moderna (5ª ed.)*<br>Katsuhiko Ogata (Pearson) | - Controladores PID en lazo cerrado<br>- Estabilidad de sistemas en tiempo continuo/discreto<br>- Sintonización de ganancias , K_d$ | **Capítulo 1:** Marco Teórico (Control clásico)<br>**Capítulo 2:** Módulo $ (PD auxiliar) |

---

## 2. Tesis de Referencia del Asesor

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `thesis.pdf` | `@phdthesis{JuarezLora2024Thesis}` | *Design and Implementation of a Neuromorphic Processing Platform for Robotic Control*<br>Dr. Jorge Alejandro Juárez Lora (CIC-IPN, 2024) | - Antecedentes directos del grupo de investigación<br>- Desafíos de cómputo en control robótico en tiempo real<br>- Evaluación de plataformas embebidas y arquitecturas de hardware | **Introducción:** Antecedentes<br>**Capítulo 1:** Marco de Referencia<br>**Capítulo 2:** Arquitectura funcional |

---

## 3. Metodología Ágil de Gestión

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `1-s2.0-S0923474821000230-main-scrum.pdf` | `@article{cano2021scrum}` | *A Scrum-based framework for new product development in the non-software industry*<br>S. Cano et al. (J. Eng. Technol. Manage.) | - Justificación de la adopción de Scrum en proyectos mecatrónicos y de hardware/investigación | **Capítulo 1:** Marco Procedimental (1.2.1 Metodología mecatrónica) |

---

## 4. Problemática Energética y Cuello de Botella Computacional

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `ajol-file-journals_...pdf` | `@article{Arikpo2007}` | *Von Neumann Architecture and Modern Computers*<br>I. Arikpo, F. Ogban, I. Eteng | - Fundamentación del cuello de botella de Von Neumann y transferencia de memoria | **Introducción:** Definición del problema (Sección 1.2) |
| `von-neumann-computer[2].pdf` | `@article{EigenmannLilja1998VonNeumann}` | *Von Neumann Computers*<br>R. Eigenmann, D. Lilja | - Limitaciones teóricas y latencias de transferencia procesador-memoria en cálculo vectorial | **Introducción:** Definición del problema |
| `PIIS2542435125001424.pdf` | `@article{deVriesGao2025AIenergy}` | *Artificial intelligence: Supply chain constraints and energy implications*<br>A. de Vries, P. Gao (Patterns, 2025) | - Impacto energético y proyecciones de consumo de modelos de IA hacia 2030 | **Introducción:** Proyección energética (Sección 1.3) |
| `Multiply accumulate operations...pdf` | `@article{Chen2021memristor}` | *Multiply accumulate operations in memristor crossbar arrays for analog computing*<br>J. Chen et al. | - Operaciones MAC (Multiplicación y Acumulación) y su costo computacional/energético | **Introducción:** Definición del problema (Sección 1.1) |

---

## 5. Técnicas de Cuantización, Poda y Optimización de Redes

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `1-s2.0-S0925231221010894-main.pdf` | `@article{Liang2021PruningSurvey}` | *Pruning and quantization for deep neural network acceleration: A survey*<br>T. Liang et al. (Neurocomputing) | - Estado del arte y taxonomía de cuantización (PTQ, QAT, simétrica/asimétrica, INT8) | **Capítulo 1:** Marco Teórico (1.1.3)<br>**Antecedentes:** Estado del arte |
| `1-s2.0-S095219762301000X-main.pdf` | `@article{Jiang2023SingleShot}` | *Single-shot pruning and quantization for hardware-friendly neural network acceleration*<br>X. Jiang et al. (EAAI) | - Cuantización orientada a aceleradores de hardware e inferencia rápida | **Capítulo 1:** Marco Teórico (1.1.3) |
| `1-s2.0-S0925231221007177-main.pdf` | `@article{LiX2021RobustnessAware}` | *Robustness-aware 2-bit quantization with real-time performance for neural network*<br>X. Li et al. (Neurocomputing) | - Impacto de la reducción de precisión en la robustez y latencia de inferencia | **Capítulo 1:** Marco Teórico (1.1.3) |
| `1-s2.0-S0920548924000758-main.pdf` | `@article{DomingoReguero2025EnergyEfficient}` | *Energy-efficient neural network training through runtime layer freezing, model quantization...*<br>D. Domingo-Reguero et al. | - Métricas cuantitativas de ahorro energético por cuantización | **Introducción:** Justificación<br>**Capítulo 1:** Marco Teórico |
| `1-s2.0-S0923596525000177-main.pdf` | `@article{ZhangL2025FLQ}` | *FLQ: Design and implementation of hybrid multi-base full logarithmic quantization...*<br>L. Zhang et al. (2025) | - Optimización de cuantización para arquitecturas de hardware | **Capítulo 1:** Marco Teórico |
| `1-s2.0-S1383762122002636-main.pdf` | `@article{Rezk2022MOHAQ}` | *MOHAQ: Multi-Objective Hardware-Aware Quantization of recurrent neural networks*<br>A. Rezk et al. (J. Syst. Arch.) | - Cuantización multi-objetivo (precisión vs latencia vs memoria) | **Capítulo 2:** Diseño Conceptual Módulo $ |
| `1-s2.0-S1383762122002727-main.pdf` | `@article{LeeYS2023ScaleCIM}` | *Scale-CIM: Precision-scalable computing-in-memory for energy-efficient quantized neural networks*<br>Y. Lee et al. (2023) | - Reducción de ancho de banda y memoria mediante modelos cuantizados | **Capítulo 1:** Marco Teórico |
| `1-s2.0-S0020025521006307-main.pdf` | `@article{Tonellotto2021QuantizationFL}` | *Neural network quantization in federated learning at the edge*<br>N. Tonellotto et al. (Inf. Sci.) | - Despliegue de cuantización en dispositivos al borde (*Edge Computing*) | **Capítulo 1:** Marco Teórico |
| `1-s2.0-S0167739X2500072X-main.pdf` | `@article{Boudjadar2025DynamicFPGA}` | *Dynamic FPGA reconfiguration for scalable embedded artificial intelligence (AI)...*<br>J. Boudjadar et al. (2025) | - Cómputo embebido para inteligencia artificial | **Capítulo 1:** Marco Teórico |

---

## 6. Robótica, Redes Neuronales y Cómputo Neuromórfico

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `electronics-14-00578-v2.pdf` | `@article{Park2025electronics}` | *Designing Spiking Neural Network-Based Reinforcement Learning for 3D Robotic Arm Applications*<br>Y. Park et al. (Electronics, 2025) | - Control de brazos robóticos manipuladores en 3D mediante redes neuronales | **Introducción:** Estado del arte<br>**Capítulo 1:** Marco Teórico (1.1.2) |
| `s41598-024-77779-8.pdf` | `@article{Zanatta2024exploring}` | *Exploring spiking neural networks for deep reinforcement learning in robotic tasks*<br>L. Zanatta et al. (Sci. Rep., 2024) | - Comparativa de precisión y consumo en tareas de robótica con redes neuronales | **Introducción:** Estado del arte |
| `1-s2.0-S0893608023003891-main.pdf` | `@article{Vlasov2023}` | *Memristor-based spiking neural network with online reinforcement learning*<br>D. Vlasov et al. (Neural Networks, 2023) | - Control neuronal en línea y aprendizaje adaptativo | **Capítulo 1:** Marco Teórico (1.1.2) |
| `FuzzyPopulationCoding.pdf` | `@article{Liu2022fuzzy}` | *Adaptive Fuzzy Population Coding Method for Spiking Neural Networks*<br>F. Liu et al. | - Codificación de señales y procesamiento para redes neuronales | **Capítulo 1:** Marco Teórico |
| `s41467-022-28487-2.pdf` | `@article{Bartolozzi2022embodied}` | *Embodied neuromorphic intelligence*<br>C. Bartolozzi, G. Indiveri, E. Donati (Nat. Commun., 2022) | - Inteligencia física incorporada (*Embodied AI*) en robótica | **Introducción:** Antecedentes |
| `s41586-024-08253-8.pdf` | `@article{Kudithipudi2025scale}` | *Neuromorphic computing at scale*<br>D. Kudithipudi et al. (Nature, 2025) | - Escalabilidad y eficiencia de arquitecturas bio-inspiradas | **Introducción:** Antecedentes |
| `jlpea-15-00015.pdf` | `@article{Zhang2025jlpea}` | *Hardware/Software Co-Design Optimization for Training Recurrent Neural Networks at the Edge*<br>Y. Zhang et al. (2025) | - Co-diseño hardware/software para redes neuronales embebidas al filo | **Capítulo 2:** Diseño Conceptual |

---

## 7. Modelado Cinemático, Dinámico y Control Analítico

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `Introduction-to-Robotics-3rd-edition.pdf` | `@book{craig2005introduction}` | *Introduction to Robotics: Mechanics and Control (3rd ed.)*<br>John J. Craig (Pearson) | - Convención Denavit-Hartenberg modificada (marcos sobre articulaciones previas)<br>- Matrices de transformación homogénea $\bm{T}_i^{i-1}$<br>- Control por par computado | **Capítulo 1:** Marco Teórico<br>**Capítulo 2:** Diseño Detallado Módulo $M_1$ y $M_2$ |
| `luh1980.pdf` | `@article{luh1980online}` | *On-Line Computational Scheme for Mechanical Manipulators*<br>J. Y. S. Luh, M. W. Walker, R. P. C. Paul (IEEE TAC, 1980) | - **Artículo seminal del algoritmo RNEA:** Pasada recursiva cinemática hacia adelante ($O(n)$) y balance de fuerzas y momentos hacia atrás | **Capítulo 1:** Marco Teórico (1.1)<br>**Capítulo 2:** Diseño Detallado Módulo $M_2$ |
| `Spong-RobotmodelingandControl.pdf` | `@book{spong2006robot}` | *Robot Modeling and Control*<br>M. Spong, S. Hutchinson, M. Vidyasagar (Wiley) | - Formulación analítica de dinámica inversa y control no lineal por par calculado (CTC) | **Capítulo 2:** Diseño Detallado Módulo $M_2$ |

---

## 8. Arquitectura de Software Robótico y Planta Manipuladora

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `710-943-00_UR3e_User_Manual_en_Global.pdf` | `@manual{universal_robots_ur3e_manual}` | *UR3e User Manual - Original Instructions (e-Series)*<br>Universal Robots A/S (2021) | - Especificaciones físicas oficiales del manipulador: alcance $500\text{ mm}$, carga $3\text{ kg}$, repetibilidad $\pm 0.03\text{ mm}$, límites de par $\pm 55\text{ Nm}$ | **Capítulo 2:** Diseño Detallado Módulo $M_1$<br>**Capítulo 3:** Implementación $M_1$ |
| `2211.07752v1.pdf` | `@article{macenski2022robot}` | *Robot Operating System 2: Design, architecture, and uses in the wild*<br>S. Macenski et al. (Science Robotics, 2022) | - Middleware ROS 2 Jazzy, comunicación determinista y arquitectura de tiempo real | **Capítulo 2:** Arquitectura funcional e Integración mecatrónica |

---

## 9. Procesamiento de Señales, Filtrado y Generación de Trayectorias

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `SavitskyGolay.pdf` | `@article{savitzky1964smoothing}` | *Smoothing and Differentiation of Data by Simplified Least Squares Procedures*<br>A. Savitzky, M. J. E. Golay (Anal. Chem., 1964) | - Filtrado digital y estimación de aceleraciones articulares analíticas $\ddot{\bm{q}}_{act}$ mediante mínimos cuadrados móviles sin amplificar ruido | **Capítulo 2:** Diseño Detallado Módulo $M_4$<br>**Capítulo 3:** Implementación $M_4$ (`bag_to_csv.py`) |
| *(Libro verificado)* | `@book{biagiotti2008trajectory}` | *Trajectory Planning for Automatic Machines and Robots*<br>L. Biagiotti, C. Melchiorri (Springer, 2008) | - Interpolación suave mediante polinomios quínticos de 5to orden ($C^2$) con aceleración nula en extremos | **Capítulo 2:** Diseño Detallado Módulo $M_4$<br>**Capítulo 3:** Implementación $M_4$ |

---

## 10. Optimización y Cuantización de Redes Neuronales

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| `1412.6980v9.pdf` | `@inproceedings{kingma2014adam}` | *Adam: A Method for Stochastic Optimization*<br>D. P. Kingma, J. Ba (ICLR, 2015) | - Algoritmo de optimización estocástica adaptativa para el entrenamiento supervisado en PyTorch (`train_pytorch.py`) | **Capítulo 2:** Diseño Detallado Módulo $M_3$<br>**Capítulo 3:** Implementación $M_3$ |
| `1712.05877v1.pdf` | `@inproceedings{jacob2018quantization}` | *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*<br>B. Jacob et al. (CVPR, 2018) | - Modelo matemático formal de cuantización afín a enteros de 8 bits (escala y *zero-point*) para inferencia determinista | **Capítulo 1:** Marco Teórico<br>**Capítulo 2:** Diseño Detallado Módulo $M_3$ |

---

## 11. Metodología de Diseño Mecatrónico y Selección Multicriterio

| Archivo PDF | Clave BibTeX | Título / Autores | Aportación al Proyecto | Sección Objetivo en TT1 |
| :--- | :--- | :--- | :--- | :--- |
| *(Libro verificado)* | `@book{pugh1991total}` | *Total Design: Integrated Methods for Successful Product Engineering*<br>Stuart Pugh (Addison-Wesley, 1991) | - Metodología de Matriz de Pugh para selección conceptual ponderada con alternativa base (*datum*) | **Capítulo 2:** Selección de diseño conceptual (Sección 2.1.6) |

