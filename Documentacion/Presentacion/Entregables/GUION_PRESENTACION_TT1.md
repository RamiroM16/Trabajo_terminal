# Guion oral para la presentación de Trabajo Terminal I

**Presentación de referencia:** Presentacion_TT1_v8, 22 diapositivas.  
**Expositor:** Ramiro Mendoza Díaz.  
**Tiempo disponible:** 20 minutos, sin preguntas.  
**Distribución propuesta:** 18 minutos 50 segundos de exposición y 1 minuto 10 segundos de margen.

Los párrafos de cada diapositiva son el texto sugerido para decir en voz alta. Las indicaciones entre corchetes sirven para ensayar y no se leen. Los tiempos son objetivos de ensayo: deben ajustarse con una lectura cronometrada. Conviene aprender la secuencia de ideas y explicar los diagramas señalándolos, en lugar de memorizar cada palabra.

## 1. Portada

**Tiempo: 0:30 · Acumulado: 0:30**

Buenos días. Se presenta el Trabajo Terminal I titulado «Control de posición de robot manipulador usando redes neuronales cuantizadas», desarrollado por Ramiro Mendoza Díaz, bajo la asesoría del doctor Jorge Alejandro Juárez Lora.

Esta etapa aborda la integración de un control neuronal en simulación y la evaluación del efecto de la cuantización sobre los recursos utilizados y el seguimiento articular. A continuación se presentan el planteamiento, la implementación y los resultados obtenidos.

## 2. Índice

**Tiempo: 0:20 · Acumulado: 0:50**

La exposición comienza con el problema y los objetivos. Después se explican los conceptos necesarios para entender la cuantización y el control neuronal. Finalmente, se presentan la implementación, la comparación experimental y las conclusiones de TT1.

## 3. Descripción del problema

**Tiempo: 0:50 · Acumulado: 1:40**

La creciente complejidad de las tareas robóticas motiva investigar diferentes métodos de control. Entre estas alternativas se encuentran las redes neuronales, cuya ejecución requiere operaciones de cómputo y transferencias de datos entre memoria y procesador.

Estas transferencias se relacionan con el cuello de botella de Von Neumann. En plataformas con recursos restringidos, especialmente sistemas móviles alimentados por baterías, también existe un presupuesto limitado de energía.

Por ello se estudia la cuantización como una alternativa para reducir los recursos utilizados, evaluando al mismo tiempo su efecto sobre la precisión del control. En TT1, esta evaluación se realizó en CPU y simulación del UR3e. La motivación energética orienta el proyecto, mientras que su medición directa queda para una etapa posterior.

## 4. Objetivo general

**Tiempo: 0:35 · Acumulado: 2:15**

El objetivo general es evaluar el desempeño energético, de precisión y de recursos utilizados al implementar un control de lazo cerrado con control tradicional y con una red neuronal cuantizada.

Para TT1 se delimitó la evaluación al seguimiento articular, al tamaño del archivo del modelo y a la latencia de inferencia en CPU. Estos resultados permiten caracterizar la implementación inicial. La evaluación energética permanece pendiente y forma parte del alcance del proyecto completo.

## 5. Objetivos específicos a cumplir en TT1

**Tiempo: 0:45 · Acumulado: 3:00**

Los objetivos específicos se resumen en cuatro actividades. Primero, investigar redes cuantizadas y metodologías de evaluación. Después, definir la arquitectura y diseñar el control neuronal base.

La siguiente actividad consiste en establecer el procedimiento de cuantización y comparación. Finalmente, se requiere preparar el plan experimental y poner en marcha la plataforma de pruebas.

La campaña presentada compara la red original en FP32 con una versión cuantizada en INT8. Esta comparación corresponde al avance experimental de TT1. La evaluación de otras precisiones y los aspectos pendientes se consideran para la siguiente etapa.

## 6. Marco teórico: FP32 e INT8

**Tiempo: 1:00 · Acumulado: 4:00**

Para entender la cuantización, primero conviene distinguir las representaciones numéricas. FP32 utiliza 32 bits por valor: un bit de signo, ocho de exponente y veintitrés de fracción. Esto equivale a cuatro bytes.

INT8 utiliza ocho bits, es decir, un byte por valor. En su representación con signo dispone de códigos enteros desde menos 128 hasta 127.

La cuantización establece una correspondencia entre valores reales y estos códigos enteros mediante una escala y un punto cero. Al disponer de menos niveles, se introduce un error de representación.

La proporción de cuatro bytes frente a uno ayuda a entender la reducción potencial por valor. En el archivo completo también intervienen otros componentes, y algunos tensores pueden conservarse en punto flotante. Por eso el tamaño final debe medirse.

## 7. Marco teórico: cuantización

**Tiempo: 1:05 · Acumulado: 5:05**

[Señalar la figura y después las ecuaciones.]

La figura, extraída del reporte, ejemplifica cómo un conjunto continuo de valores se representa mediante niveles discretos. Es una ilustración conceptual del proceso.

Con ocho bits se dispone de 256 códigos posibles. La escala, representada por S, determina la separación entre niveles. El punto cero, Z, indica el código asociado al cero real.

Para cuantizar un valor, se divide entre la escala, se redondea y se incorpora el punto cero. La operación de recorte mantiene el resultado dentro del rango entero disponible. La última expresión permite reconstruir una aproximación del valor real.

La diferencia entre el valor original y el reconstruido es el error de cuantización. En una aplicación de control interesa observar cómo esta modificación de la representación se refleja en el comportamiento del sistema.

## 8. Marco teórico: redes neuronales

**Tiempo: 0:40 · Acumulado: 5:45**

En una red de capas densas, cada capa combina sus entradas mediante pesos y sesgos. Las funciones de activación permiten representar relaciones no lineales.

Para este proyecto, las entradas describen el estado del robot y la referencia de movimiento, mientras que las salidas corresponden a los torques articulares.

El diagrama muestra el principio de funcionamiento. La topología utilizada se presenta más adelante. La cuantización modifica la representación numérica de las operaciones y los parámetros, conservando la estructura de la red.

## 9. Marco teórico: ONNX

**Tiempo: 0:40 · Acumulado: 6:25**

ONNX permite describir el modelo mediante un grafo de operadores y tensores para intercambiarlo entre herramientas compatibles.

En el proyecto, la red se entrenó en PyTorch y se exportó a un archivo ONNX. Posteriormente, ONNX Runtime permitió ejecutar la inferencia desde C++ e integrarla con el control.

La distinción es que ONNX describe el modelo y ONNX Runtime lo ejecuta. Esta separación permitió utilizar el mismo flujo de integración para comparar las versiones FP32 e INT8.

## 10. Entorno de simulación

**Tiempo: 0:45 · Acumulado: 7:10**

La plataforma de evaluación utiliza el manipulador UR3e, con seis grados de libertad, en Gazebo Harmonic. La integración se realizó con ROS 2 Jazzy y ros2_control, y la inferencia se ejecutó en CPU.

El control interno se configuró nominalmente a 500 hertz. Las referencias y la recopilación de datos se realizaron a 100 hertz. Estas tasas corresponden a funciones diferentes dentro de la implementación.

La captura ilustra el entorno utilizado. Los resultados que se presentan después corresponden a las métricas de la campaña experimental. La evaluación de esta etapa se limita a simulación.

## 11. Control RNEA + PD

**Tiempo: 1:05 · Acumulado: 8:15**

[Señalar las dos ramas que llegan a la suma.]

La primera configuración combina un cálculo dinámico mediante el algoritmo recursivo de Newton-Euler, o RNEA, con una acción proporcional y derivativa.

RNEA utiliza la posición y velocidad actuales, junto con la aceleración deseada, para calcular una contribución dinámica. La rama PD utiliza los errores de posición y velocidad para generar una corrección en torque.

El error de posición se define como la referencia menos la posición actual. De forma equivalente, el error de velocidad es la velocidad deseada menos la velocidad actual.

Ambas contribuciones se suman para obtener el torque total aplicado. Esta configuración proporciona la referencia de comparación y el torque objetivo utilizado para entrenar la red. La corrección PD se incorpora en torque, como muestra la ecuación.

## 12. Topología de la red implementada

**Tiempo: 1:00 · Acumulado: 9:15**

La red implementada es un perceptrón multicapa con 42 entradas y seis salidas. Sus capas ocultas tienen 256, 512, 256 y 128 neuronas, respectivamente.

Esta estructura contiene 307 mil 590 parámetros entrenables, considerando pesos y sesgos. Entre las capas ocultas se utilizan activaciones ReLU.

Las 42 entradas reúnen información del estado articular, las referencias de movimiento y la contribución dinámica calculada por RNEA. Las seis salidas corresponden a los torques objetivo, uno por articulación.

La comparación FP32 frente a INT8 conserva esta topología. Esto permite estudiar el cambio en la representación numérica sobre la misma arquitectura, sin introducir una reducción adicional del número de neuronas.

## 13. Control con red neuronal

**Tiempo: 1:20 · Acumulado: 10:35**

[Recorrer el diagrama de izquierda a derecha y señalar la realimentación.]

Durante la ejecución se construye el vector de entrada a partir de las referencias y del estado del robot. RNEA también aporta una característica dinámica a este vector.

Las entradas se normalizan antes de pasar por la red. La inferencia produce una salida que después se desnormaliza para recuperar los torques en sus unidades físicas. A continuación se aplica una saturación provisional y se envían los torques al robot virtual.

La posición y velocidad obtenidas en simulación se realimentan para preparar las entradas de la siguiente actualización.

En esta arquitectura la red se entrena para obtener el torque total. Por ello, la salida desnormalizada se utiliza directamente como comando de torque. La contribución RNEA ya participa como información de entrada y no se suma nuevamente a esa salida.

La saturación uniforme de más y menos 55 newton metro se utilizó como simplificación en simulación. Su adecuación por articulación deberá revisarse antes de una implementación física.

## 14. Datos y tratamiento de la aceleración

**Tiempo: 1:15 · Acumulado: 11:50**

Las 42 características corresponden a siete grupos de seis variables: posición, velocidad y aceleración actuales, sus referencias deseadas y el torque calculado por RNEA.

Aquí se reconoce una diferencia entre entrenamiento y despliegue. Para el entrenamiento se utilizó aceleración actual obtenida mediante procesamiento y filtrado. Durante la ejecución del control neuronal, esa aceleración se fijó a cero como simplificación. La aceleración deseada sí se conserva.

Esta diferencia modifica la información disponible para la red y debe revisarse en la siguiente etapa. Los resultados actuales no permiten cuantificar de forma aislada su contribución al error de seguimiento.

Se plantea investigar un método de estimación de aceleración con bajo costo computacional. Su evaluación deberá considerar tanto el seguimiento como el tiempo añadido a la preparación de entradas y al ciclo completo del control.

## 15. Cuantización dinámica implementada

**Tiempo: 1:00 · Acumulado: 12:50**

El procedimiento aplicado fue cuantización dinámica posterior al entrenamiento. Primero se entrenó el modelo en punto flotante y se exportó a ONNX. Después se generó su versión cuantizada.

En este procedimiento, los pesos se cuantizan fuera de línea. Los parámetros de cuantización de las activaciones, como la escala y el punto cero, se calculan durante la inferencia.

De esta manera se obtuvo la versión INT8 utilizada en la comparación. El entrenamiento consciente de la cuantización, conocido como QAT, queda como una alternativa para investigar posteriormente.

El efecto de este procedimiento se evaluó con las mediciones de tamaño, latencia de inferencia y seguimiento articular que se muestran a continuación.

## 16. Condiciones y métricas de comparación

**Tiempo: 1:00 · Acumulado: 13:50**

La comparación incluye tres configuraciones: control RNEA más PD, control con red FP32 y control con red INT8.

Se utilizaron trayectorias articulares quínticas en simulación, con ejecución en CPU y recopilación de datos a 100 hertz. La figura muestra un perfil quíntico ilustrativo extraído del reporte y sirve para explicar el tipo de referencia empleado.

Para evaluar el seguimiento se utilizó la raíz del error cuadrático medio, o RMSE, expresada en radianes. También se midió la latencia de inferencia y el tamaño del archivo ONNX.

Estas métricas permiten contrastar los recursos utilizados con la precisión obtenida. Cada resultado debe interpretarse según lo que mide: tamaño del archivo, ejecución de la inferencia o seguimiento del robot.

## 17. Tamaño del archivo ONNX

**Tiempo: 0:45 · Acumulado: 14:35**

El archivo FP32 tiene un tamaño de 1232 kilobytes, mientras que el archivo INT8 tiene 315 kilobytes. Esto representa una reducción del 74.43 por ciento.

Este resultado supera el criterio de reducción de al menos 50 por ciento establecido para el tamaño del modelo.

La medición corresponde al archivo almacenado en disco. La memoria utilizada durante la ejecución incluye otros componentes del programa y requiere una evaluación propia. Con estos datos se demuestra la reducción del archivo ONNX bajo el procedimiento aplicado.

## 18. Latencia media de inferencia

**Tiempo: 1:00 · Acumulado: 15:35**

La latencia media de inferencia pasó de 37.1 microsegundos en FP32 a 29.2 microsegundos en INT8. La reducción observada fue del 21.29 por ciento.

La comparación utiliza la misma etapa de ejecución en ambos modelos: la inferencia aislada en CPU. El control completo también incluye el cálculo RNEA, la preparación de entradas y el procesamiento de las salidas, además de la interacción con la plataforma.

Por ello, estas mediciones acreditan una menor latencia media de inferencia bajo las condiciones experimentales empleadas. La caracterización del tiempo total y de su variación permanece pendiente.

El siguiente resultado permite revisar si esta reducción estuvo acompañada de un seguimiento articular equivalente.

## 19. Seguimiento articular

**Tiempo: 1:20 · Acumulado: 16:55**

[Señalar cada barra y después la línea de referencia.]

El control RNEA más PD obtuvo un RMSE de 0.063 radianes. La red FP32 obtuvo 0.092 radianes y la red INT8 obtuvo 0.138 radianes.

En la campaña evaluada, el control analítico presentó el menor error de seguimiento y la versión INT8 presentó el mayor. Por tanto, la reducción del archivo y de la latencia debe valorarse junto con este resultado de precisión.

El criterio RF-01 establece un RMSE menor a 0.05 radianes. Ninguna de las tres configuraciones alcanzó ese criterio. Los valores obtenidos se conservan como referencia de desempeño para la siguiente etapa.

La diferencia observada entre FP32 e INT8 tampoco permite atribuir todo el error exclusivamente a la cuantización. También deben investigarse las condiciones de entrenamiento y las diferencias en las entradas durante el despliegue.

Se requiere mejorar el seguimiento y evaluar estas contribuciones antes de establecer una conclusión sobre la precisión de una implementación posterior.

## 20. Cumplimiento y limitaciones

**Tiempo: 1:00 · Acumulado: 17:55**

La tabla reúne los resultados y los aspectos pendientes. El criterio de reducción del archivo se cumplió, con 74.43 por ciento. También se observó una reducción del 21.29 por ciento en la latencia media de inferencia en CPU.

El criterio de seguimiento no se alcanzó. La medición trazable del ciclo completo y del jitter, entendido como la variación temporal de las ejecuciones, permanece por verificar.

El consumo eléctrico también está pendiente de medición directa. Además, la saturación uniforme de torque requiere una revisión por articulación antes de su uso físico.

Esta evaluación delimita el avance de TT1 y permite establecer las prioridades de la siguiente etapa con base en los resultados obtenidos.

## 21. Conclusiones de TT1

**Tiempo: 0:45 · Acumulado: 18:40**

En TT1 se integró y evaluó un control con red neuronal para el manipulador en simulación. La cuantización INT8 redujo el tamaño del archivo ONNX y la latencia media de inferencia observada en CPU.

El seguimiento articular requiere mejora, ya que ninguna configuración alcanzó RF-01. También se documentó la diferencia en el tratamiento de la aceleración entre entrenamiento y despliegue.

Para TT2, las prioridades son mejorar la precisión, caracterizar el tiempo total del control y evaluar directamente el consumo energético. Los resultados de TT1 proporcionan una base experimental para orientar ese trabajo.

## 22. Referencias y cierre

**Tiempo: 0:10 · Acumulado: 18:50**

Las referencias del reporte y de la documentación técnica utilizada se muestran en esta diapositiva. Gracias por su atención. Queda abierta la sesión de preguntas.

---

## Respuestas de respaldo para preguntas del jurado

Estas respuestas se preparan para la discusión posterior. No se agregan a la exposición de 20 minutos.

### ¿Por qué se eligió 0.05 radianes?

El valor se adoptó en el documento como una meta exploratoria de seguimiento. No se realizó un estudio específico para seleccionar ese límite ni se cuenta con una referencia normativa que lo justifique. Su fundamentación según una tarea concreta permanece pendiente. Se mantiene explícito que ninguna configuración alcanzó ese criterio.

**Si se pregunta por su origen:** el valor fue sugerido inicialmente por Gemini durante el apoyo a la redacción y se incorporó como meta. Ese origen no constituye sustento técnico. La conversión a aproximadamente 2.86 grados permite interpretar su magnitud, pero no justifica su elección.

### Si la red recibe RNEA, ¿para qué se utiliza la red?

La arquitectura estudiada utiliza el resultado de RNEA como una característica dinámica, junto con el estado y las referencias. La red se entrenó para obtener el torque total generado por el control de referencia. Esta implementación permite evaluar el comportamiento del control neuronal y su cuantización. Como RNEA sigue formando parte de la preparación de entradas, la reducción de su costo computacional no se puede atribuir a la comparación de inferencia aislada. Se necesita medir el control completo.

### ¿La red aprende dinámica no modelada?

La evidencia presentada corresponde al aprendizaje del torque total de la configuración de referencia. Para demostrar compensación de dinámica no modelada se requiere un diseño experimental y datos que permitan identificar esa contribución. Esa afirmación no se establece con los resultados actuales.

### ¿Por qué la aceleración actual se fijó a cero?

Se utilizó como simplificación durante el despliegue. Esto introduce una diferencia respecto a los datos de entrenamiento, donde la aceleración actual se obtuvo mediante procesamiento y filtrado. Se reconoce como una limitación. Se plantea evaluar un estimador de bajo costo y medir su efecto sobre el seguimiento y el tiempo total de ejecución.

### ¿INT8 es mejor que FP32?

En esta campaña, INT8 produjo un archivo menor y una menor latencia media de inferencia. También presentó un RMSE mayor. La conveniencia depende de los requisitos de precisión y recursos de la aplicación. Los resultados actuales muestran ese compromiso y todavía requieren mejora del seguimiento.

### ¿Se demostró ahorro energético?

No se realizó una medición directa de consumo eléctrico en TT1. Se midieron el tamaño del archivo y la latencia de inferencia, que deben mantenerse como resultados separados. Para evaluar energía se requiere instrumentación y una metodología de medición bajo condiciones comparables.

### ¿Se garantiza que el control cumple sus tiempos?

Se cuenta con mediciones de inferencia bajo la configuración experimental utilizada. La frecuencia nominal de actualización y una media de inferencia reducida no acreditan por sí solas el cumplimiento temporal de todas las ejecuciones. Queda pendiente caracterizar el ciclo completo y su variación mediante registros trazables.

### ¿Qué representa el valor de 151.2 microsegundos?

Corresponde a la ejecución del control RNEA más PD integrado. Los 29.2 microsegundos de INT8 corresponden a inferencia aislada. Son alcances de medición diferentes. Por eso la gráfica compara FP32 e INT8 en la misma etapa, usando 37.1 y 29.2 microsegundos.

### ¿Por qué se utilizó el mismo límite de torque en todas las articulaciones?

Se utilizó por facilidad de implementación durante las pruebas iniciales en simulación. Es una simplificación provisional. Antes de una implementación física deben revisarse los límites apropiados para cada articulación y las condiciones de operación.

## Indicaciones para el ensayo

1. Realizar una primera lectura en voz alta y registrar el tiempo por diapositiva. Incluir las pausas para señalar figuras y cambiar de lámina.
2. Usar como referencias de avance el minuto 7:10 al terminar el entorno de simulación, 13:50 antes de los resultados y 17:55 antes de las conclusiones.
3. Si se supera el tiempo, acortar primero el marco teórico. Conservar la explicación del torque total, la diferencia en la aceleración y la interpretación de los resultados.
4. Practicar los números principales y sus unidades: 307,590 parámetros, 1232 y 315 KB, 37.1 y 29.2 µs, y los tres RMSE en radianes.
5. Ensayar las respuestas de respaldo sin leerlas. Cuando un aspecto no se haya medido, delimitar la evidencia disponible y explicar el trabajo pendiente.
