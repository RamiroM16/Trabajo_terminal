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
