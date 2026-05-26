# Trabajo Práctico N°1 — Análisis Exploratorio de Datos (EDA)

## Dataset

**Stack Overflow Developer Survey 2023**

- Fuente: [https://survey.stackoverflow.co/2023/](https://survey.stackoverflow.co/2023/)
- Archivo requerido: `survey_results_public.csv`
- Filas originales: ~89.184 | Columnas utilizadas: 13

## Requisitos

```
python >= 3.10
pandas
numpy
matplotlib
seaborn
```

Instalación rápida:

```bash
pip install pandas numpy matplotlib seaborn
```

## Estructura del proyecto

```
EDA_StackOverflow_2023.ipynb   ← Notebook principal
survey_results_public.csv      ← Dataset (descargar por separado)
README.md                      ← Este archivo
```

## Cómo ejecutar

1. Descargar el dataset desde [survey.stackoverflow.co/2023](https://survey.stackoverflow.co/2023/) y colocar `survey_results_public.csv` en la misma carpeta que el notebook.
2. Abrir `EDA_StackOverflow_2023.ipynb` en Jupyter Notebook o JupyterLab.
3. Ejecutar todas las celdas en orden (Kernel → Restart & Run All).

## Hipótesis planteadas

| # | Hipótesis |
|---|-----------|
| H1 | Los desarrolladores con más años de experiencia profesional tienen salarios más altos. |
| H2 | El nivel educativo más alto se asocia con salarios más altos. |
| H3 | Los desarrolladores en organizaciones más grandes tienden a tener salarios mayores. |
| H4 | Los Data Scientists / ML Engineers tienen el salario promedio más alto entre los roles técnicos. |
| H5 | La experiencia en programación (años codificando) tiene mayor correlación con el salario que la experiencia profesional (años trabajando). |

## Contenido del notebook

| Sección | Descripción |
|---------|-------------|
| 0 | Importación de librerías |
| 1 | Carga del dataset y selección de columnas |
| 2 | Hipótesis a explorar |
| 3 | Limpieza de datos |
| 4.1 | Descripción estadística (dtypes, describe) |
| 4.2 | Histogramas con KDE |
| 4.3 | Boxplots por categoría |
| 4.4 | Scatterplots con línea de tendencia y correlación de Pearson |
| 4.5 | Gráficos adicionales (barras, evolución salarial) |
| 4.6 | Mapa de calor de correlaciones |
| 5 | Verificación de hipótesis |
| 6 | Conclusiones finales |

## Columnas utilizadas

| Columna | Descripción |
|---------|-------------|
| `Country` | País del encuestado |
| `EdLevel` | Nivel educativo alcanzado |
| `YearsCode` | Años totales escribiendo código |
| `YearsCodePro` | Años de experiencia profesional como desarrollador |
| `DevType` | Tipo de rol (puede ser múltiple, se simplifica) |
| `OrgSize` | Tamaño de la organización |
| `ConvertedCompYearly` | Salario anual en USD (normalizado por Stack Overflow) |
| `Age` | Rango etario |
| `Employment` | Situación laboral |
| `LanguageHaveWorkedWith` | Lenguajes usados en el último año |
| `OpSysProfessional` | Sistema operativo en entorno profesional |
| `AISearchHaveWorkedWith` | Herramientas de IA utilizadas |
| `MentalHealth` | Estado de salud mental autorreportado |
