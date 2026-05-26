# Trabajo Práctico N°1 — Análisis Exploratorio de Datos (EDA)

**Dataset:** Stack Overflow Developer Survey 2025  
**Herramientas:** Python · Pandas · NumPy · Matplotlib · Seaborn

---

## Objetivo

El objetivo de este trabajo es aplicar técnicas de Análisis Exploratorio de Datos (EDA) sobre un dataset real de gran escala para caracterizar la industria del desarrollo de software a nivel global en 2025. A través de visualizaciones, estadísticas descriptivas y verificación de hipótesis, se busca comprender la distribución del salario anual de desarrolladores en función de variables como la experiencia, la modalidad de trabajo, el nivel educativo, el tamaño de la organización y el tipo de rol. El análisis sigue un flujo completo: limpieza de datos → descripción univariada y bivariada → visualización → verificación de hipótesis → conclusiones.

---

## Contexto del Dataset

La **Stack Overflow Developer Survey** es una encuesta anual realizada por Stack Overflow, la plataforma de preguntas y respuestas más grande del mundo para desarrolladores de software. Desde 2011, recopila datos sobre hábitos, herramientas, salarios, condiciones laborales y perfil sociodemográfico de la comunidad global de programadores.

La edición **2025** contó con la participación de **49.191 encuestados** de más de 180 países. Los datos son de acceso público y distribuidos bajo licencia Open Database License (ODbL).

- **Fuente oficial:** [https://survey.stackoverflow.co/](https://survey.stackoverflow.co/)
- **Repositorio GitHub:** [https://github.com/StackExchange/Survey](https://github.com/StackExchange/Survey)
- **Archivo:** `stackoverflow_results_2025.csv`
- **Filas:** 49.191 (dataset completo, sin muestreo)
- **Columnas totales:** 172 | **Columnas utilizadas en el análisis:** 13

### Cómo obtener el dataset

1. Ingresar a [https://survey.stackoverflow.co/](https://survey.stackoverflow.co/) o al repositorio de GitHub
2. Descargar `stackoverflow_results_2025.csv`
3. Colocarlo en la misma carpeta que el notebook

---

## Diccionario de Datos

| Columna | Tipo original | Descripción | Transformación aplicada |
|---------|--------------|-------------|------------------------|
| `ResponseId` | int | Identificador único de cada respuesta | Sin transformación; usado como índice de control |
| `Age` | string | Rango etario del encuestado (ej.: "25-34 years old") | Sin transformación; uso descriptivo |
| `Country` | string | País de residencia del encuestado | Sin transformación; top-10 países en visualizaciones |
| `EdLevel` | string | Nivel educativo máximo alcanzado (texto largo) | Mapeado a etiquetas cortas: Primaria, Secundaria, Univ. sin título, Tecnicatura, Licenciatura, Maestría, Doctorado / PhD |
| `Employment` | string | Situación laboral (puede contener múltiples valores separados por `;`) | Uso descriptivo; no desagregado |
| `RemoteWork` | string | Modalidad de trabajo (Presencial / Híbrido / Remoto / A elección) | Mapeado a 5 categorías legibles; 31,3 % de nulos (solo para respuestas con dato disponible) |
| `YearsCode` | string/float | Años de experiencia programando (incluye "Less than 1 year" y "More than 50 years") | Convertido a float: "Less than 1 year" → 0.5, "More than 50 years" → 50.0; función `limpiar_anios()` |
| `WorkExp` | float | Años de experiencia laboral total | Mismo tratamiento que `YearsCode`; 12,8 % de nulos |
| `ConvertedCompYearly` | float | Salario anual en USD normalizado por Stack Overflow (ajuste PPP) | Filtrado: > USD 1.000 y ≤ percentil 99 (umbral: USD 450.000) para eliminar valores implausibles y outliers extremos |
| `DevType` | string | Tipo de rol profesional (puede contener múltiples valores separados por `;`) | Simplificado a categoría única por prioridad con función `simplificar_devtype()`: Data Scientist/ML, Full-stack, Back-end, Front-end, DevOps/SRE, etc. |
| `OrgSize` | string | Tamaño de la organización empleadora (texto largo) | Mapeado a etiquetas cortas ordenadas: Solo, 2-9, 10-19, 20-99, 100-499, 500-999, 1K-5K, 5K-10K, +10K |
| `JobSat` | float | Satisfacción laboral autorreportada (escala 0–10) | Sin transformación; 45,8 % de nulos |
| `AISelect` | string | Frecuencia de uso de herramientas de IA en el trabajo | Sin transformación; uso descriptivo |

---

## Metodología

### 1. Carga y selección de datos

Se cargó el dataset completo (49.191 filas, 172 columnas) y se seleccionaron las 13 columnas relevantes para los objetivos del análisis. No se realizó ningún muestreo previo para preservar la representatividad del dataset.

### 2. Limpieza de datos

- **Valores nulos:** Se contabilizaron los nulos por columna. `ConvertedCompYearly` presenta el mayor porcentaje (51,3 %), ya que muchos encuestados no reportan su salario (desempleados, estudiantes, quienes prefieren no revelar ingresos). Se decidió trabajar con un subconjunto `df_sal` específicamente para los análisis salariales.
- **Duplicados:** Se verificó la ausencia de filas duplicadas — los 49.191 `ResponseId` son todos únicos.
- **Conversión de tipos:** Las columnas `YearsCode` y `WorkExp` contenían strings con casos especiales. Se creó la función `limpiar_anios()` para convertirlas a `float`.
- **Variables multi-valor:** `DevType` puede contener múltiples roles separados por `;`. Se aplicó la función `simplificar_devtype()` que asigna una única categoría primaria por orden de prioridad.
- **Estandarización de etiquetas:** `EdLevel` y `OrgSize` contenían strings extensos. Se aplicaron diccionarios de mapeo (`EDLEVEL_MAP`, `ORGSIZE_MAP`) para obtener etiquetas cortas con un orden lógico.
- **Subset salarial (`df_sal`):** Para los análisis de salario se creó un subconjunto filtrado (salarios > USD 1.000 y ≤ percentil 99), resultando en 22.981 registros válidos con una mediana de USD 76.412 y una media de USD 90.357.

### 3. Análisis descriptivo

- Revisión de tipos de datos (`dtypes`) y estadísticas básicas (`describe`) para variables numéricas y categóricas.
- Distribución de las 5 variables categóricas principales: `RemoteWork`, `EdLevel_short`, `DevType_simp`, `OrgSize_short`, `AISelect`.

### 4. Visualizaciones

| Tipo | Variables analizadas |
|------|---------------------|
| Histograma + KDE | `ConvertedCompYearly` (salario), `YearsCode` (exp. profesional), `WorkExp` (exp. laboral total) |
| Boxplot | Salario por `RemoteWork` (modalidad); por `EdLevel` (nivel educativo); por `OrgSize` (tamaño de empresa) |
| Scatterplot | Salario vs. `YearsCode`; Salario vs. `WorkExp` |
| Barras horizontales | Top 10 países por cantidad de participantes; salario mediano por `DevType` |
| Línea con banda IQR | Evolución del salario mediano por tramo de experiencia profesional |
| Mapa de calor | Matriz de correlación de Pearson entre variables numéricas |

Para los scatterplots se utilizó una muestra aleatoria de 5.000 registros (`random_state=42`) para evitar sobreploteo, junto con una línea de tendencia calculada con `np.polyfit` y el coeficiente de correlación de Pearson anotado en el gráfico.

### 5. Verificación de hipótesis

Cada hipótesis se evaluó mediante análisis descriptivo comparativo: agrupaciones con `groupby`, medianas por categoría y correlación de Pearson. No se aplicaron pruebas de significancia estadística formal, en línea con el enfoque exploratorio del trabajo.

---

## Hipótesis planteadas

| # | Hipótesis |
|---|-----------|
| H1 | Los desarrolladores con más años de experiencia profesional tienen salarios significativamente más altos. |
| H2 | El trabajo remoto está asociado a salarios más altos que el trabajo presencial. |
| H3 | El nivel educativo formal influye positivamente en el salario. |
| H4 | Los desarrolladores en empresas más grandes ganan más que los de empresas pequeñas. |
| H5 | Existen diferencias salariales significativas según el tipo de desarrollador (DevType). |

---

## Conclusiones y Hallazgos Relevantes

### H1 — Experiencia profesional y salario ✅ Confirmada

La relación entre experiencia profesional y salario es positiva, consistente y marcada. La mediana salarial crece en todos los tramos: de USD 12.470 para quienes tienen 0-2 años de experiencia hasta USD 105.577 para quienes superan los 20 años. La correlación de Pearson entre `YearsCode` y `ConvertedCompYearly` es de **r = 0.364**, positiva y moderada, lo que confirma la tendencia aunque señala que la experiencia no es el único determinante del salario.

### H2 — Modalidad de trabajo y salario ✅ Confirmada

El trabajo remoto presenta la mediana salarial más alta del conjunto: **USD 90.491**, frente a USD 47.566 para el trabajo completamente presencial. El trabajo híbrido se ubica en posiciones intermedias (USD 73.375 – USD 81.210). Esto sugiere que el trabajo remoto está correlacionado con roles de mayor seniority o con empresas de mayor escala global que ofrecen mejores compensaciones.

### H3 — Nivel educativo y salario ✅ Parcialmente confirmada

La relación entre nivel educativo y salario existe, pero no es perfectamente monotónica. Quienes tienen Doctorado presentan la mediana más alta (USD 88.171), seguidos por Maestría (USD 81.210) y Licenciatura (USD 78.714). Sin embargo, el grupo "Univ. sin título" (USD 69.310) supera a Tecnicatura (USD 70.769) y se acerca a los graduados universitarios, mientras que Primaria muestra una mediana sorprendentemente alta (USD 64.408) por el escaso número de casos. Esto evidencia que en la industria del software, la experiencia práctica puede compensar la formación académica formal.

### H4 — Tamaño de empresa y salario ✅ Confirmada

La tendencia es clara y robusta: a mayor tamaño de organización, mayor salario mediano. Las empresas de más de 10.000 empleados presentan la mediana más alta del conjunto (**USD 100.000**), mientras que las de 20-99 empleados muestran la más baja entre las categorías con suficientes datos (USD 69.764). La brecha total entre el segmento menor y el mayor supera los USD 30.000 anuales en mediana.

### H5 — Tipo de desarrollador y diferencias salariales ✅ Confirmada

Existen diferencias salariales significativas entre roles. El **Engineering Manager** lidera el ranking con una mediana de **USD 127.677**, seguido por Security Engineer (USD 102.316) y DevOps / SRE (USD 87.011). En el extremo opuesto, Data Analyst (USD 58.367) y Front-end Developer (USD 63.808) registran las medianas más bajas entre los roles técnicos. La brecha entre el rol mejor y peor remunerado supera los USD 69.000 anuales, confirmando que el tipo de rol es uno de los factores más determinantes del salario.

### Hallazgos adicionales

- **Distribución salarial sesgada positivamente:** La distribución de `ConvertedCompYearly` presenta fuerte asimetría positiva. La mediana (USD 76.412) es considerablemente menor que la media (USD 90.357), lo que indica que una minoría con salarios muy altos eleva el promedio. La mediana es el estadístico más adecuado para describir el ingreso típico en este dataset.
- **Alta adopción de IA en 2025:** Una mayoría de encuestados reporta usar herramientas de IA diariamente (15.883 respuestas) o semanalmente (5.958). Solo 5.454 encuestados no usan IA y no planean hacerlo, lo que refleja la consolidación definitiva de estas herramientas en el flujo de trabajo del desarrollo de software.
- **Concentración geográfica:** EE.UU. representa más del 15 % de las respuestas totales y concentra los salarios más altos, lo que introduce un sesgo en los valores absolutos reportados. El análisis salarial debe interpretarse con esta limitación en mente.
- **Alta tasa de nulos en salario:** El 51,3 % de los encuestados no reportó su salario. El subconjunto `df_sal` (22.981 filas) puede no ser representativo de toda la población encuestada, especialmente de quienes trabajan en regiones con salarios bajos o en situación de desempleo.

---

## Estructura del repositorio

```
EDA_StackOverflow_2025_Sawin.ipynb   ← Notebook principal con todo el análisis
stackoverflow_results_2025.csv       ← Dataset (descargar por separado)
README_2025.md                       ← Este archivo
```

## Cómo ejecutar

```bash
pip install pandas numpy matplotlib seaborn
jupyter notebook EDA_StackOverflow_2025_Sawin.ipynb
```

Ejecutar todas las celdas en orden (Kernel → Restart & Run All). El dataset debe estar en la misma carpeta que el notebook.
