# Repositorio de Artículos Científicos y Literatura Técnica (PDF)

Esta carpeta contiene el corpus de literatura científica y libros de referencia para el Trabajo Terminal.

---

## 1. Catálogo Maestro Indexado
Para consultar qué artículos están disponibles, sus metadatos completos y qué sección específica de `TT1.tex` fundamentan, revisa el archivo:
* 👉 **[`catalogo_articulos.md`](file:///home/ramiro/.gemini/antigravity/worktrees/Trabajo_terminal/analyze_current_project/Documentacion/Articulos/catalogo_articulos.md)**

---

## 2. Contenido del Repositorio (26 Documentos PDF)
1. **Libros Canónicos de Fundamentos:** Spong (*Robot Modeling and Control*), Lynch & Park (*Modern Robotics*), Ogata (*Ingeniería de Control Moderna*), Barrientos (*Fundamentos de Robótica*).
2. **Tesis Doctoral del Asesor:** Dr. Jorge Alejandro Juárez Lora (*Design and Implementation of a Neuromorphic Processing Platform for Robotic Control*, CIC-IPN).
3. **Metodología Ágil:** Scrum en proyectos de ingeniería (Cano et al.).
4. **Problemática de Cómputo y Energía:** Von Neumann bottleneck, consumo energético de IA hacia 2030 (Nature, Patterns).
5. **Cuantización y Optimización de Redes:** Surveys de poda y cuantización (Liang et al.), PTQ/QAT (Jiang et al.), cuantización al filo (Tonellotto et al., Rezk et al.).
6. **Robótica y Control Neuronal:** Control de brazos robóticos 3D con redes neuronales (Park et al., Zanatta et al., Vlasov et al.).

---

## 3. Estrategia de Consulta de los Agentes
Los agentes **no cargan los 26 PDFs simultáneamente** para no saturar su contexto. En su lugar:
* Consultan el catálogo [`catalogo_articulos.md`](file:///home/ramiro/.gemini/antigravity/worktrees/Trabajo_terminal/analyze_current_project/Documentacion/Articulos/catalogo_articulos.md).
* Cuando se redacta una sección específica (ej. dinámica RNEA en el Capítulo 1 o selección del UR3e en el Capítulo 2), invocan un subagente efímero que extrae el fragmento exacto del PDF relevante con `pdftotext`.
