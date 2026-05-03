import pandas as pd
import joblib

# Load models and scalers
model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")
scaler_young = joblib.load("artifacts/scaler_young.joblib")
scaler_rest = joblib.load("artifacts/scaler_rest.joblib")


def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split(" & ")
    total_score = sum(risk_scores.get(d, 0) for d in diseases)

    return total_score / 14


def preprocess_input(input_dict):

    # ❌ NO income_level here
    expected_columns = [
        'age', 'number_of_dependants',
        'income_lakhs',
        'insurance_plan', 'genetical_risk',
        'normalized_risk_score',
        'gender_Male',
        'region_Northwest', 'region_Southeast', 'region_Southwest',
        'marital_status_Unmarried',
        'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight',
        'smoking_status_Occasional', 'smoking_status_Regular',
        'employment_status_Salaried', 'employment_status_Self-Employed'
    ]

    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    # -------- Numerical --------
    df['age'] = input_dict['age']
    df['number_of_dependants'] = input_dict['number_of_dependants']
    df['income_lakhs'] = input_dict['income_lakhs']
    df['genetical_risk'] = input_dict['genetical_risk']

    # Insurance encoding
    plan_map = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df['insurance_plan'] = plan_map.get(input_dict['insurance_plan'], 1)

    # -------- Categorical --------
    if input_dict['gender'] == 'Male':
        df['gender_Male'] = 1

    if input_dict['region'] == 'Northwest':
        df['region_Northwest'] = 1
    elif input_dict['region'] == 'Southeast':
        df['region_Southeast'] = 1
    elif input_dict['region'] == 'Southwest':
        df['region_Southwest'] = 1

    if input_dict['marital_status'] == 'Unmarried':
        df['marital_status_Unmarried'] = 1

    if input_dict['bmi_category'] == 'Obesity':
        df['bmi_category_Obesity'] = 1
    elif input_dict['bmi_category'] == 'Overweight':
        df['bmi_category_Overweight'] = 1
    elif input_dict['bmi_category'] == 'Underweight':
        df['bmi_category_Underweight'] = 1

    if input_dict['smoking_status'] == 'Occasional':
        df['smoking_status_Occasional'] = 1
    elif input_dict['smoking_status'] == 'Regular':
        df['smoking_status_Regular'] = 1

    if input_dict['employment_status'] == 'Salaried':
        df['employment_status_Salaried'] = 1
    elif input_dict['employment_status'] == 'Self-Employed':
        df['employment_status_Self-Employed'] = 1

    # -------- Risk --------
    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['medical_history'])

    # -------- Scaling --------
    df = handle_scaling(df)

    return df


def handle_scaling(df):

    age = df['age'].iloc[0]

    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    # ✅ create income_level ONLY for scaling
    df['income_level'] = df['income_lakhs']

    # ensure all required columns exist
    for col in cols_to_scale:
        if col not in df.columns:
            df[col] = 0

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # ❗ REMOVE before prediction
    if 'income_level' in df.columns:
        df.drop('income_level', axis=1, inplace=True)

    return df


def predict(input_dict):

    input_df = preprocess_input(input_dict)

    if input_dict['age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])