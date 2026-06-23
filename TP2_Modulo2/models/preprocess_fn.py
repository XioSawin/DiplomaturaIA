def preprocess(df, is_train=True):
    """Aplica todas las transformaciones de feature engineering.
    Retorna DataFrame procesado sin el target.
    """
    df = df.copy()

    # --- Eliminar ID (no predictivo) ---
    df = df.drop(columns=['ID'], errors='ignore')

    # --- Feature Engineering ---

    # BMI
    df['BMI'] = df['weight(kg)'] / (df['height(cm)'] / 100) ** 2

    # Presión de pulso (diferencial)
    df['pulse_pressure'] = df['systolic'] - df['relaxation']

    # Razón HDL/Colesterol (indica calidad del colesterol)
    df['HDL_ratio'] = df['HDL'] / (df['Cholesterol'] + 1e-6)

    # Transformaciones log para variables con skew positivo
    for col in ['triglyceride', 'Gtp', 'ALT', 'AST', 'serum creatinine',
                'fasting blood sugar', 'LDL', 'Cholesterol']:
        df[f'log_{col}'] = np.log1p(df[col])

    # Binning de edad
    df['age_group'] = pd.cut(df['age'], bins=[0, 35, 45, 55, 65, 100],
                              labels=[0, 1, 2, 3, 4]).astype(int)

    # Interacción: gender × hemoglobin (los hombres tienen mayor hemoglobina y fuman más)
    df['gender_num'] = (df['gender'] == 'M').astype(int)
    df['gender_hemo'] = df['gender_num'] * df['hemoglobin']

    # --- Codificar categóricas ---
    df['gender'] = df['gender'].map({'M': 1, 'F': 0}).astype(int)
    df['oral']   = df['oral'].map({'Y': 1, 'N': 0}).astype(int)
    df['tartar'] = df['tartar'].map({'Y': 1, 'N': 0}).astype(int)

    return df
