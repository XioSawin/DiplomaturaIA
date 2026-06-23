# TP2 - Módulo 2: Predicción de Fumadores

## Descripción del Proyecto

Modelo de Machine Learning para predecir si una persona es fumadora o no (`smoking`: 0/1) a partir de datos de chequeos de salud (indicadores biométricos y de laboratorio).

**Métrica objetivo:** F1-Score para la clase 1 (fumadores).

---

## Resultados Finales

| Métrica | Valor |
|---------|-------|
| F1-Score clase 1 (test) | **0.7297** |
| ROC-AUC (test) | ~0.88 |
| Accuracy (test) | 0.76 |
| Modelo | XGBoost (optimizado con RandomizedSearchCV) |
| Umbral de clasificación | 0.48 |

---

## Estructura del Proyecto

```
TP2_Modulo2/
├── data/
│   ├── raw/              # Datos originales (.xlsx)
│   ├── processed/        # X_train, X_test, y_train, y_test (.csv)
│   └── external/         # predicciones_finales.csv
├── models/
│   ├── xgb_model.joblib      # Modelo XGBoost entrenado
│   ├── scaler.joblib          # StandardScaler
│   ├── threshold.joblib       # Umbral óptimo de clasificación
│   ├── feature_names.joblib   # Lista de features
│   └── preprocess_fn.py       # Función de preprocesamiento
├── notebooks/
│   ├── 01_lectura_y_discovery.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocesamiento.ipynb
│   ├── 04_entrenamiento_y_optimizacion.ipynb
│   ├── 05_validacion.ipynb
│   └── 06_prediccion.ipynb
├── requirements.txt
└── README.md
```

---

## Dataset

- **Etiquetado (entrenamiento):** 50.000 filas, 26 features + target `smoking`
- **Sin etiquetar (predicción):** 5.692 filas, 26 features
- **Target:** `smoking` — 0: no fumador (63%), 1: fumador (37%)
- **Sin valores faltantes**

### Variables del dataset

| Variable | Descripción |
|----------|-------------|
| gender | Sexo (M/F) |
| age | Edad en años |
| height(cm), weight(kg) | Antropometría |
| waist(cm) | Circunferencia de cintura |
| eyesight(left/right) | Agudeza visual |
| hearing(left/right) | Audición |
| systolic, relaxation | Presión arterial |
| fasting blood sugar | Glucemia en ayuno |
| Cholesterol, HDL, LDL, triglyceride | Perfil lipídico |
| hemoglobin | Hemoglobina |
| Urine protein | Proteína en orina |
| serum creatinine | Creatinina sérica |
| AST, ALT, Gtp | Enzimas hepáticas |
| oral | Examen oral (Y/N) |
| dental caries | Caries (0/1) |
| tartar | Sarro dental (Y/N) |

---

## Cómo reproducir el entorno

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar notebooks en orden
jupyter notebook
# → notebooks/01_lectura_y_discovery.ipynb
# → notebooks/02_eda.ipynb
# → notebooks/03_preprocesamiento.ipynb
# → notebooks/04_entrenamiento_y_optimizacion.ipynb
# → notebooks/05_validacion.ipynb
# → notebooks/06_prediccion.ipynb
```

---

## Descripción de cada Notebook

### 01 - Lectura y Discovery
Carga de los dos datasets, exploración de tipos de datos, valores faltantes y distribución del target.

### 02 - EDA (Análisis Exploratorio)
Visualización de variables categóricas y numéricas vs. el target. Mapa de correlaciones e identificación de las variables más predictivas (`hemoglobin`, `gender`, `height`, `weight`, `Gtp`, `ALT`).

### 03 - Preprocesamiento y Feature Engineering
- Eliminación de `ID` (no predictivo)
- **Nuevas features creadas:**
  - `BMI` = peso / altura²
  - `pulse_pressure` = sistólica − diastólica
  - `HDL_ratio` = HDL / colesterol
  - Transformaciones log de variables con distribución sesgada (triglyceride, Gtp, ALT, etc.)
  - `age_group` (binning en 5 grupos)
  - `gender_hemo` (interacción sexo × hemoglobina)
- Codificación de variables categóricas (binary mapping)
- Escalado con `StandardScaler` (fit solo en train)
- Split estratificado 80/20 con `random_state=42`

### 04 - Entrenamiento y Optimización
**Modelos comparados (baseline):**
| Modelo | F1-Test |
|--------|---------|
| Decision Tree | ~0.68 |
| KNN | ~0.66 |
| Random Forest | ~0.71 |
| **XGBoost** | **~0.72** |

XGBoost fue el modelo con mejor desempeño. Se realizó una búsqueda aleatoria (`RandomizedSearchCV`) con 60 iteraciones y 5-fold CV optimizando F1 para clase 1, explorando:
- `n_estimators`, `max_depth`, `learning_rate`
- `subsample`, `colsample_bytree`, `min_child_weight`
- `reg_alpha`, `reg_lambda`, `scale_pos_weight`

Se ajustó además el **umbral de clasificación** (0.48) para maximizar el F1-Score de clase 1.

### 05 - Validación
Evaluación completa del modelo final: classification report, matrices de confusión, curva ROC (AUC ~0.88), curva Precisión-Recall y distribución de probabilidades predichas.

### 06 - Predicción Final
Carga del modelo entrenado, aplica el **mismo pipeline** al dataset sin etiquetar y exporta `predicciones_finales.csv` con la columna `smoking_prediction` (valores 0 o 1).

---

## Conclusiones

1. **XGBoost superó** a Decision Tree, KNN y Random Forest en F1 para clase 1.
2. Las variables más importantes fueron **hemoglobin**, **gender_hemo**, **height(cm)**, **weight(kg)**, **log_Gtp** y **waist(cm)**.
3. El dataset está **desbalanceado** (~63%/37%). Se manejó usando `scale_pos_weight` y ajustando el umbral de clasificación.
4. El **feature engineering** (BMI, pulse pressure, log transforms, gender×hemoglobin) aportó mejoras medibles al F1.
5. El umbral óptimo fue **0.48** (ligeramente inferior a 0.5), favoreciendo el recall de la clase minoritaria.
