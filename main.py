import streamlit as st
from prediction_helper import predict


st.set_page_config(page_title="Insurance Predictor", layout="wide")


st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 18px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'>💊 Health Insurance Cost Predictor</h1>", unsafe_allow_html=True)
st.markdown("---")


st.sidebar.header("ℹ️ Instructions")
st.sidebar.write("Fill all details and click Predict")

categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}


st.subheader("👤 Personal Details")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input('Age', 18, 100)
with col2:
    number_of_dependants = st.number_input('Dependants', 0, 20)
with col3:
    income_lakhs = st.number_input('Income (Lakhs)', 0, 200)


st.subheader("📊 Risk & Plan")
col4, col5, col6 = st.columns(3)

with col4:
    genetical_risk = st.number_input('Genetical Risk', 0, 5)
with col5:
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
with col6:
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])


st.subheader("🏃 Lifestyle")
col7, col8, col9 = st.columns(3)

with col7:
    gender = st.selectbox('Gender', categorical_options['Gender'])
with col8:
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
with col9:
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

st.subheader("🏥 Health Details")
col10, col11, col12 = st.columns(3)

with col10:
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
with col11:
    region = st.selectbox('Region', categorical_options['Region'])
with col12:
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'])


input_dict = {
    'age': age,
    'number_of_dependants': number_of_dependants,
    'income_lakhs': income_lakhs,
    'genetical_risk': genetical_risk,
    'insurance_plan': insurance_plan,
    'employment_status': employment_status,
    'gender': gender,
    'marital_status': marital_status,
    'bmi_category': bmi_category,
    'smoking_status': smoking_status,
    'region': region,
    'medical_history': medical_history
}

st.markdown("---")

# Predict button
col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])

with col_btn2:
    if st.button('🚀 Predict Insurance Cost'):
        try:
            prediction = predict(input_dict)
            st.success(f'💰 Estimated Cost: ₹ {round(prediction, 2)}')
        except Exception as e:
            st.error(f"Error: {e}")

st.write("NEW VERSION 003")