## Documentación del Proyecto: Análisis de Sentimiento en Tweets (Sentiment140)


### 1. Objetivo del Proyecto

El objetivo principal de este proyecto es desarrollar y evaluar diferentes modelos de clasificación de sentimiento para tweets, utilizando el dataset Sentiment140. Se busca identificar qué enfoques (modelos pre-entrenados, Bag of Words, TF-IDF, Word2Vec) ofrecen el mejor rendimiento para esta tarea, prestando especial atención a la capacidad de los modelos para manejar diferentes clases de sentimiento (positivo, negativo, y neutral en el set de prueba).

### 2. Instalación de dependencias e Imports (Sección 0)

Se instalaron las bibliotecas necesarias (`kagglehub`, `wordcloud`, `umap-learn`, `keybert`, `gensim`) y se importaron las librerías estándar para manipulación de datos (`pandas`, `numpy`), visualización (`matplotlib`, `seaborn`), procesamiento de lenguaje natural (`nltk`, `TextBlob`, `gensim`), y aprendizaje automático (`sklearn`). Se configuró un `random.seed` para reproducibilidad.

### 3. Carga de Datos y Parámetros Generales (Sección 1)

- **Parámetro `USE_SAMPLE`**: Se definió un parámetro `USE_SAMPLE = False` para indicar que el proyecto se ejecutaría utilizando el **dataset completo de 1.6 millones de tweets**. Esto asegura que los modelos se entrenen con la mayor cantidad de datos posible para obtener un rendimiento robusto.
- **Rutas de Datos**: Se montó Google Drive para acceder a los archivos del dataset (`training.1600000.processed.noemoticon.csv` y `testdata.manual.2009.06.14.csv`).
- **Carga de DataFrames**: El dataset principal (`df`) contiene 1.6 millones de tweets con etiquetas de sentimiento 0 (negativo) y 4 (positivo). El `df_test_manual` es un conjunto de prueba más pequeño (498 tweets) que **sí incluye la clase neutral (2)**.
- **Verificación del Dataset**: Se confirmó que se estaba trabajando con el dataset completo de 1.6 millones de tweets, como se estableció en el parámetro `USE_SAMPLE`.

### 4. Análisis Exploratorio de Datos (EDA) (Sección 2)

El EDA se realizó para entender la estructura y características de los datos:
- **Valores nulos y duplicados**: Se verificó que no existían valores nulos ni duplicados en el dataset.
- **Distribución de clases**: El dataset de entrenamiento (`df`) contiene un 50% de tweets negativos (0) y un 50% de tweets positivos (4). El `df_test_manual` incluye las clases 0, 2 y 4.
- **Longitud de tweets**: La longitud promedio de los tweets es de aproximadamente 74 caracteres, con una distribución que muestra que la mayoría de los tweets utilizan cerca de la mitad de los 140 caracteres disponibles en Twitter (ahora X) en 2009.
- **Palabras más frecuentes y distintivas**: Se identificaron las palabras más frecuentes y las más distintivas para cada clase de sentimiento (positivo y negativo) después de eliminar stopwords. Esto proporcionó una visión inicial de los términos asociados a cada sentimiento. Algo interesante es que las palabras más frecuentes antes de la limpieza son "hashtags" y probablemente estén relacionado a campañas de visibilidad del momento.
- **Atributos derivados**: Se crearon atributos como la longitud del texto, el conteo de URLs, hashtags y menciones. Se observó que los tweets positivos tienden a tener más URLs, hashtags y menciones. También se extrajeron el día de la semana y la hora del tweet, mostrando cómo el sentimiento varía a lo largo del día y la semana.

### 5. Preprocesamiento de Texto (Sección 3)

Se aplicó una función `limpieza_rapida` para preparar el texto de los tweets:
- **Normalización**: Conversión a minúsculas.
- **Eliminación de elementos no textuales**: URLs y menciones (@usuario) fueron eliminadas.
- **Manejo de hashtags**: El símbolo '#' se reemplazó por un espacio, manteniendo la palabra clave.
- **Filtrado de caracteres**: Se eliminaron caracteres no alfabéticos y se normalizaron espacios.
- **Eliminación de stopwords y tokens cortos**: Se removieron palabras comunes (stopwords en inglés) y tokens de una sola letra, buscando reducir ruido y enfocarse en términos con mayor peso semántico.

### 6. División de Datos (Sección 4)

- **Split estratificado**: El dataset `df` (tweets limpios y etiquetas 0/4) se dividió en conjuntos de entrenamiento (`X_train`, `y_train`) y validación (`X_val`, `y_val`) en una proporción 90/10. La estratificación aseguró que la proporción de clases se mantuviera en ambos conjuntos.
- **Conjunto de prueba manual**: `X_test_manual` y `y_test_manual` (que incluye las clases 0, 2 y 4) se reservaron para la evaluación final. Este conjunto es fundamental para evaluar cómo los modelos se comportan con la clase neutral, que no está presente en el entrenamiento del resto de los modelos.

### 7. Modelo Baseline: TextBlob (Sección 5)

- **TextBlob**: Se utilizó TextBlob como modelo baseline pre-entrenado. TextBlob no requiere entrenamiento con nuestro dataset, ya que se basa en léxicos y reglas para determinar la polaridad de un texto.
- **Funciones de clasificación**: Se definieron funciones para convertir la polaridad de TextBlob a clases binarias (0/4) y ternarias (0/2/4, para el `df_test_manual`).
- **Evaluación**: TextBlob se evaluó sobre muestras del conjunto de entrenamiento y validación (en clasificación binaria) y, crucialmente, sobre el `df_test_manual` (en clasificación ternaria). Los resultados se registraron para comparación. TextBlob obtuvo una `accuracy_test_manual` de 0.620482 y un `f1_macro_test_manual` de 0.611692.

### 8. Modelos Entrenados (Secciones 6, 7 y 8)

Se entrenaron tres modelos basados en diferentes representaciones de texto y clasificadores:

#### 8.1. Modelo 1: Bag of Words (BoW) + Naive Bayes (Sección 6)
- **Vectorización**: `CountVectorizer` se usó para crear una representación BoW, considerando 50,000 `max_features` y `ngram_range=(1, 1)` (unigramas).
- **Clasificador**: Se entrenó un `MultinomialNB` (Naive Bayes Multinomial) con las características BoW.
- **Resultados**: El modelo alcanzó una `accuracy_train` de 0.778, `accuracy_val` de 0.767 y `accuracy_test_manual` de 0.584. Se observa una caída significativa en la `accuracy_test_manual` debido a la incapacidad de clasificar la clase neutral (0.00 en `precision`, `recall`, `f1-score` para la clase 2).

#### 8.2. Modelo 2: TF-IDF + Regresión Logística (SGD) (Sección 7)
- **Vectorización**: `TfidfVectorizer` se utilizó con 100,000 `max_features`, `ngram_range=(1, 2)` (unigramas y bigramas) y `sublinear_tf=True` para ajustar la importancia de las palabras.
- **Clasificador**: Se empleó un `SGDClassifier` con `loss="log_loss"` (equivalente a regresión logística) y 20 `max_iter`.
- **Resultados**: Obtuvo una `accuracy_train` de 0.758, `accuracy_val` de 0.756 y `accuracy_test_manual` de 0.568. Al igual que el modelo BoW+NB, mostró un rendimiento nulo en la clase neutral del test manual.

#### 8.3. Modelo 3: Word2Vec + Clasificador (Sección 8)
- **Entrenamiento de Word2Vec**: Se entrenó un modelo `Word2Vec` Skip-gram (`sg=1`) sobre el corpus completo de tweets limpios (`tokenized`). Se utilizaron `vector_size=200`, `window=5`, `min_count=5` y `epochs=5`. El vocabulario aprendido fue de 51,545 palabras.
- **Vectorización de tweets**: Cada tweet se representó como el promedio de los embeddings Word2Vec de sus tokens.
- **Clasificador**: Se entrenó una `LogisticRegression` con los embeddings promedio de los tweets.
- **Resultados**: Este modelo obtuvo una `accuracy_train` de 0.739, `accuracy_val` de 0.738 y `accuracy_test_manual` de 0.590. También presentó la limitación de no clasificar la clase neutral.

### 9. Comparación de Resultados (Sección 9)

- **Tabla `resultados_df`**: Se consolidaron los resultados de todos los modelos en un DataFrame, ordenados por `accuracy_test_manual`. 

| modelo                   | entrenado_con                            | accuracy_train | f1_macro_train | accuracy_val | f1_macro_val | accuracy_test_manual | f1_macro_test_manual |
|:-------------------------|:-----------------------------------------|:---------------|:---------------|:-------------|:-------------|:---------------------|:---------------------|
| TextBlob (pre-entrenado) | — (no se entrena; muestra de train/val) | 0.602200       | 0.560568       | 0.599200     | 0.557434     | 0.620482             | 0.611692             |
| Word2Vec + LogReg        | 1440000 tweets                           | 0.739370       | 0.739347       | 0.738750     | 0.738727     | 0.590361             | 0.458449             |
| BoW + Naive Bayes        | 1440000 tweets                           | 0.778108       | 0.778098       | 0.767406     | 0.767399     | 0.584337             | 0.454814             |
| TF-IDF + SGD/LogReg      | 1440000 tweets                           | 0.758922       | 0.758841       | 0.756000     | 0.755913     | 0.568273             | 0.446231             |

- **Análisis**: El **TextBlob (pre-entrenado)** fue el modelo con mejor rendimiento en el `accuracy_test_manual` (0.62), a pesar de que los modelos entrenados mostraron mayor precisión en los conjuntos de train y validación. Esto se debe a la inclusión de la clase neutral en el conjunto de prueba manual, la cual TextBlob sí puede manejar, mientras que los modelos entrenados no fueron expuestos a ella.
- **Curva de aprendizaje**: Se analizaron las curvas de aprendizaje para BoW+NB y TF-IDF+SGD, mostrando que el aumento del tamaño del set de entrenamiento generalmente mejora la precisión, aunque con rendimientos decrecientes a partir de cierto punto.
- **Intervalos de confianza (bootstrap)**: Se calcularon intervalos de confianza del 95% para el accuracy de cada modelo en el `df_test_manual` mediante bootstrap. Esto ayuda a entender la variabilidad de la métrica debido al tamaño limitado del conjunto de prueba. Los resultados confirmaron a TextBlob como el de mejor rendimiento con un intervalo de confianza más favorable.
- **Matriz de confusión del mejor modelo**: Se visualizó la matriz de confusión para TextBlob, mostrando su rendimiento en la clasificación de las clases 0, 2 y 4 en el test manual.

### 10. Métrica Obligatoria: Similitud Coseno y PPMI (Sección 10)

Se exploraron las relaciones semánticas capturadas por el modelo Word2Vec:
- **Similitud Coseno**: Se calculó la similitud coseno entre palabras clave de sentimiento (positivas vs. negativas). Por ejemplo, `good` vs `bad` (0.504), `love` vs `hate` (0.402), y `good` vs `sad` (0.312). Estos valores moderados a bajos sugieren que el modelo diferencia correctamente entre palabras con sentimientos opuestos, aunque algunas pueden co-ocurrir en contextos de contraste.
- **Analogías**: Se probó una analogía como `good - happy + sad`. Los resultados (`saaaaad`, `tearful`, `dissapointing`) son coherentes con la expectativa de encontrar palabras relacionadas con la tristeza, lo que indica que el modelo capturó relaciones semánticas complejas.
- **PPMI**: Se construyó una matriz de co-ocurrencias y se calculó el PPMI. `PPMI(good, great)` (21.70) y `PPMI(good, bad)` (21.52) mostraron valores altos. Esto indica que ambas parejas de palabras co-ocurren frecuentemente. Un PPMI alto para `good` y `bad` sugiere que estas palabras aparecen juntas en contextos de contraste o comparación, más que una similitud directa de significado.

### 11. Extras Opcionales (Sección 11)

- **Wordclouds por sentimiento**: Se generaron nubes de palabras para tweets positivos y negativos, visualizando los términos más prominentes en cada categoría.
- **Visualización UMAP de embeddings**: Se utilizó UMAP para reducir la dimensionalidad de los embeddings Word2Vec de una muestra de tweets a 2D y visualizarlos, coloreados por sentimiento. Esto permite observar si los clusters de tweets de diferentes sentimientos son distinguibles en el espacio de embeddings.
- **Extracción de keywords con BERT (KeyBERT)**: Se usó KeyBERT para extraer palabras clave de muestras de tweets positivos y negativos.

### 12. Conclusiones Finales (Sección 12)

#### 12.1 Resumen de resultados
- **Mejor modelo**: **TextBlob (pre-entrenado)**, según `accuracy_test_manual` (0.620482), superando a los modelos entrenados (BoW+NB, TF-IDF+SGD, Word2Vec+LogReg) en el conjunto de prueba que incluye la clase neutral.

#### 12.2 Justificación de las decisiones tomadas
- **Preprocesamiento**: Se optó por una limpieza exhaustiva para eliminar ruido específico de Twitter y enfocar el análisis en palabras clave. La eliminación de stopwords y tokens cortos es estándar para la mayoría de los modelos de texto.
- **Vectorización (BoW / TF-IDF)**: Se eligieron diferentes configuraciones de `max_features` y `ngram_range` para explorar el impacto de la granularidad en la representación. BoW con unigramas es simple pero efectivo, mientras que TF-IDF con bigramas busca capturar más contexto.
- **Word2Vec**: Se entrenó un modelo Skip-gram con un tamaño de vector de 200, buscando un equilibrio entre detalle semántico y eficiencia. Se mencionó la posibilidad de experimentar con más epochs, diferentes tamaños de vector, o embeddings pre-entrenados como mejoras futuras.
- **Muestreo**: Los modelos principales se entrenaron con el dataset **completo** (1.6M de tweets) al establecer `USE_SAMPLE = False`. Sin embargo, para tareas computacionalmente intensivas como la validación de TextBlob (5k tweets), la construcción de la matriz PPMI (100k tweets) y la visualización UMAP (5k tweets), se utilizaron muestras. Esto se hizo para optimizar el tiempo de ejecución y los recursos, sin afectar la robustez del entrenamiento de los modelos principales.

#### 12.3 Comparación contra el modelo pre-entrenado (TextBlob)
- TextBlob superó a los modelos entrenados en el `df_test_manual` principalmente porque **fue capaz de clasificar la clase neutral (2)**, mientras que nuestros modelos (entrenados solo con clases 0 y 4) no pudieron. Los modelos entrenados tuvieron `precision`, `recall` y `f1-score` de 0.00 para la clase 2, lo que penalizó significativamente sus métricas generales en el test manual.

#### 12.4 Interpretación de la métrica de embeddings (coseno / PPMI)
- Las métricas de embeddings mostraron que Word2Vec capturó relaciones semánticas coherentes. Palabras con sentimientos opuestos mostraron similitudes coseno moderadas a bajas, mientras que PPMI elevado entre palabras como 'good' y 'bad' sugiere que a menudo co-ocurren en contextos de comparación o contraste.

#### 12.5 Análisis de errores
- El análisis de errores sistemático del modelo TextBlob reveló que los errores se agrupan en categorías como 'Negación', 'Contraste / posible sarcasmo', y 'Sentimiento mixto', además de 'Otro / jerga / sin patrón claro'. Esto destaca los desafíos inherentes al análisis de sentimiento en textos complejos de redes sociales.

#### 12.6 Limitaciones y Futuras Mejoras
- **Ausencia de clase neutral en entrenamiento**: La principal limitación es que los modelos entrenados no vieron ejemplos de la clase neutral. Una mejora fundamental sería obtener o crear un dataset de entrenamiento que incluya la clase 2 para que los modelos puedan aprender a identificarla.
- **Antigüedad del dataset**: El dataset es de 2009. El lenguaje de Twitter ha evolucionado, por lo que los modelos pueden no generalizar bien a tweets modernos. Se podría explorar la recopilación de datos más recientes o el uso de embeddings pre-entrenados más actuales.
- **Complejidad de los errores**: Los errores sistemáticos (`negación`, `contraste/sarcasmo`, `sentimiento mixto`) sugieren que los modelos, incluso TextBlob, tienen dificultades con la sutileza del lenguaje. Futuras mejoras podrían incluir el uso de modelos más sofisticados (como Transformers) o la incorporación de reglas específicas para manejar estas complejidades.
- **Exploración de parámetros**: Podríamos explorar más a fondo los hiperparámetros de los modelos (ej. `max_features` para vectorizadores, `vector_size` y `epochs` para Word2Vec) o probar arquitecturas de redes neuronales más avanzadas para el procesamiento de texto.
