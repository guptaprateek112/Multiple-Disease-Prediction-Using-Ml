
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime


st.markdown(
    """
    <style>
    /* Page gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Segoe UI', sans-serif;
        color: white;
        min-height: 100vh;
        padding: 2rem;
        position: relative;
        overflow: hidden;
    }

    /* Floating blobs */
    .stApp::before, .stApp::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        filter: blur(90px);
        opacity: 0.6;
        z-index: 0;
    }

    .stApp::before {
        width: 300px;
        height: 300px;
        background: #5ee7df;
        top: 20%;
        left: 70%;
    }

    .stApp::after {
        width: 250px;
        height: 250px;
        background: #9f5afd;
        bottom: 10%;
        left: -100px;
    }
    
    /* Heartbeat animation */
    .heartbeat {
        width: 100px;
        height: 100px;
        margin: 20px auto;
        stroke: #ff3860;
        stroke-width: 3;
        fill: none;
        animation: heartbeat 1.5s ease-in-out infinite;
        display: block;
    }

    @keyframes heartbeat {
        0%, 100% {
            stroke-dashoffset: 300;
            stroke-dasharray: 300;
            opacity: 0.5;
    }
    50% {
        stroke-dashoffset: 0;
        stroke-dasharray: 300;
        opacity: 1;
        }
    }


    /* Central block container */
    .block-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        padding: 2rem 3rem;
        max-width: 900px;
        margin: auto;
        z-index: 2;
        position: relative;
        animation: fadeIn 1s ease forwards;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }

    h1, h2, h3 {
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
    }

    /* Neon button */
    .stButton>button {
        background-color: transparent;
        border: 2px solid #5ee7df;
        color: #5ee7df;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #5ee7df;
        color: black;
        box-shadow: 0 0 20px #5ee7df;
    }

    /* Inputs & dropdowns */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {
        background: rgba(255,255,255,0.1);
        border: none;
        border-radius: 10px;
        padding: 10px;
        color: white;
    }

    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>div:focus {
        outline: none;
        box-shadow: 0 0 10px #5ee7df;
    }

    /* Sidebar style */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255,255,255,0.1);
        box-shadow: inset -5px 0 15px rgba(0,0,0,0.2);
        color: white;
    }

    /* Sidebar text and widget styling */
    .sidebar-content {
        padding: 1rem;
    }

    .sidebar .css-1d391kg {  /* sidebar header */
        color: white;
        font-weight: bold;
    }

    .sidebar .stButton>button {
        border-color: #9f5afd;
        color: #9f5afd;
    }

    .sidebar .stButton>button:hover {
        background: #9f5afd;
        color: black;
        box-shadow: 0 0 10px #9f5afd;
    }

    /* Fade in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)





# 🔐 Authentication Config
hashed_passwords = stauth.Hasher(['123456789']).generate()

config = {
    'credentials': {
        'usernames': {
            'demo': {
                'email': 'demo@gmail.com',
                'name': 'Demo User',
                'password': hashed_passwords[0]
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'some_signature_key',
        'name': 'some_cookie_name'
    },
    'preauthorized': {
        'emails': ['demo@gmail.com']
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# 🔐 Login Widget
name, auth_status, username = authenticator.login('Login', 'main')

# 🔑 User Authenticated
if auth_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f'Welcome {name}')
    
    st.write("Logged in successfully!")

    st.title(" Multiple Disease Prediction System")
    st.write("Use machine learning to predict common diseases.")

    # ✅ Load Models
    with open('models/diabetes_model.sav', 'rb') as file:
        diabetes_model = pickle.load(file)
    with open('models/heart_model.sav', 'rb') as file:
        heart_disease_model = pickle.load(file)
    with open('models/parkinsons_model.sav', 'rb') as file:
        parkinsons_model = pickle.load(file)

    # 🧭 Sidebar Navigation
    with st.sidebar:
        selected = option_menu(
        menu_title='Disease Predictor',
        options=['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Disease Prediction'],
        icons=['activity', 'heart-pulse', 'virus'],
        default_index=0,
        key='main_menu'  
        
    )
    # 🩺 Pages


    # -----------------------------------------------
    # 🩸 DIABETES PREDICTION
    # -----------------------------------------------
    # ----------------------------
    if selected == 'Diabetes Prediction':
        st.header('🩸 Diabetes Prediction')
        col1, col2, col3 = st.columns(3)
        with col1:
            Pregnancies = st.number_input('Pregnancies', min_value=0, max_value=20)
            SkinThickness = st.number_input('Skin Thickness', min_value=0, max_value=100)
            DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=3.0)
        with col2:
            Glucose = st.number_input('Glucose', min_value=0, max_value=300)
            Insulin = st.number_input('Insulin', min_value=0, max_value=900)
            Age = st.number_input('Age', min_value=1, max_value=120)
        with col3:
            BloodPressure = st.number_input('Blood Pressure', min_value=0, max_value=180)
            BMI = st.number_input('BMI', min_value=0.0, max_value=70.0)

        if st.button('Predict Diabetes'):
            user_data = [[Pregnancies, Glucose, BloodPressure, SkinThickness,
                          Insulin, BMI, DiabetesPedigreeFunction, Age]]
            prediction = diabetes_model.predict(user_data)[0]

            st.subheader("🧬 Prediction Result")
            if prediction == 1:
                st.error("The model predicts that this patient is likely to have **Diabetes**.")
            else:
                st.success("The model predicts that this patient is unlikely to have **Diabetes**.")

                # 🧾 Improved PDF generation
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                
                # Header
                c.setFont("Helvetica-Bold", 18)
                c.drawString(50, 770, "🧬 Diabetes Prediction Report")
                c.setFont("Helvetica", 12)
                c.drawString(50, 750, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Prediction result
                c.setFont("Helvetica-Bold", 14)
                result_text = "⚠️ Likely to have Diabetes" if prediction == 1 else "✅ Unlikely to have Diabetes"
                c.drawString(50, 720, f"Prediction Result: {result_text}")
                
                # Patient Data
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, 690, "Patient Input Summary:")
                c.setFont("Helvetica", 11)
                patient_data = [
                    f"Pregnancies: {Pregnancies}",
                    f"Glucose: {Glucose}",
                    f"Blood Pressure: {BloodPressure}",
                    f"Skin Thickness: {SkinThickness}",
                    f"Insulin: {Insulin}",
                    f"BMI: {BMI}",
                    f"Diabetes Pedigree Function: {DiabetesPedigreeFunction}",
                    f"Age: {Age}",
                ]
                
                y = 670
                for item in patient_data:
                    c.drawString(60, y, item)
                    y -= 15
                
                # Explanation of risk factors
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y - 10, "Risk Factor Highlights:")
                y -= 30
                c.setFont("Helvetica", 11)
                risk_factors = [
                    f"🔹 Glucose ({Glucose}): {'High Risk' if Glucose >= 140 else 'Normal'}",
                    f"🔹 BMI ({BMI}): {'Overweight' if BMI >= 30 else 'Healthy'}",
                    f"🔹 Age ({Age}): {'Senior Risk Group' if Age >= 45 else 'Low Risk'}",
                    f"🔹 Pedigree Function ({DiabetesPedigreeFunction}): {'High Genetic Risk' if DiabetesPedigreeFunction >= 0.5 else 'Low Genetic Risk'}"
                ]
                for factor in risk_factors:
                    c.drawString(60, y, factor)
                    y -= 15
                
                # Recommendations
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y - 10, "Recommendations:")
                y -= 30
                c.setFont("Helvetica", 11)
                recommendations = (
                    [
                        "🩺 Please consult a doctor for further evaluation.",
                        "🍎 Maintain a low-sugar diet, increase physical activity.",
                        "🧪 Regularly monitor glucose and HbA1c levels.",
                        "👟 Aim for at least 30 minutes of moderate exercise daily.",
                    ] if prediction == 1 else [
                        "👍 Continue healthy lifestyle habits.",
                        "🏃‍♂️ Stay active to reduce risk of diabetes in the future.",
                        "🥗 Monitor diet and keep regular checkups for early detection."
                    ]
                )
                for tip in recommendations:
                    c.drawString(60, y, tip)
                    y -= 15
                
                # Footer
                c.setFont("Helvetica-Oblique", 9)
                c.drawString(50, 50, "This report was generated using an AI-based prediction model. Consult a physician for clinical advice.")
                
                c.save()
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Detailed Diabetes PDF Report",
                    data=buffer,
                    file_name="diabetes_detailed_report.pdf",
                    mime="application/pdf"
                )



            st.markdown(f"""
            ### 🔍 Explanation:
            - **Glucose**: {Glucose} ({'High' if Glucose >= 140 else 'Normal'} risk)
            - **BMI**: {BMI} ({'Overweight' if BMI >= 30 else 'Healthy'} risk)
            - **Age**: {Age} ({'Senior' if Age >= 45 else 'Young'} group)
            - **Pedigree Function**: {DiabetesPedigreeFunction} ({'High' if DiabetesPedigreeFunction >= 0.5 else 'Low'} genetic risk)

            ### 📌 Next Steps:
            - ✅ Maintain a healthy lifestyle if not at risk.
            - ⚠️ Consult a doctor if you're at risk. Monitor glucose, diet, and activity levels regularly.
            """)

    # -----------------------------
    # ❤️ Heart Disease Prediction
    # -----------------------------
    elif selected == 'Heart Disease Prediction':
        st.header("❤️ Heart Disease Prediction")

        sex_map = {'Male': 1, 'Female': 0}
        cp_map = {'Typical Angina': 0, 'Atypical Angina': 1, 'Non-anginal Pain': 2, 'Asymptomatic': 3}
        fbs_map = {'Yes': 1, 'No': 0}
        restecg_map = {'Normal': 0, 'ST-T Abnormality': 1, 'Left Ventricular Hypertrophy': 2}
        exang_map = {'Yes': 1, 'No': 0}
        slope_map = {'Upsloping': 0, 'Flat': 1, 'Downsloping': 2}
        thal_map = {'Normal': 1, 'Fixed Defect': 2, 'Reversible Defect': 3}

        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input('Age', min_value=1, max_value=120)
            trestbps = st.number_input('Resting Blood Pressure')
            chol = st.number_input('Cholesterol')
            oldpeak = st.number_input('ST Depression')
            ca = st.selectbox('Major Vessels Colored (0-3)', [0, 1, 2, 3])
        with col2:
            sex = st.selectbox('Sex', list(sex_map.keys()))
            fbs = st.selectbox('Fasting Blood Sugar > 120?', list(fbs_map.keys()))
            exang = st.selectbox('Exercise Induced Angina', list(exang_map.keys()))
            slope = st.selectbox('ST Segment Slope', list(slope_map.keys()))
            thal = st.selectbox('Thalassemia', list(thal_map.keys()))
        with col3:
            cp = st.selectbox('Chest Pain Type', list(cp_map.keys()))
            restecg = st.selectbox('Resting ECG Result', list(restecg_map.keys()))
            thalach = st.number_input('Max Heart Rate')

        if st.button("Predict Heart Disease"):
           
            features = [[
                age, sex_map[sex], cp_map[cp], trestbps, chol, fbs_map[fbs],
                restecg_map[restecg], thalach, exang_map[exang], oldpeak,
                slope_map[slope], ca, thal_map[thal]
            ]]
            prediction = heart_disease_model.predict(features)[0]
            st.subheader("🫀 Prediction Result")
            if prediction == 1:
                st.error("The model predicts that this patient is likely to have **Heart Disease**.")
            else:
                st.success("The model predicts that this patient is unlikely to have **Heart Disease**.")
                # PDF generation
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                
            
                c.setFont("Helvetica-Bold", 18)
                c.drawString(50, 770, "🫀 Heart Disease Prediction Report")
                c.setFont("Helvetica", 12)
                c.drawString(50, 750, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
                result_text = "⚠️ Likely to have Heart Disease" if prediction == 1 else "✅ Unlikely to have Heart Disease"
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, 720, f"Prediction Result: {result_text}")
            
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, 690, "Patient Input Summary:")
                patient_data = [
                    f"Age: {age}", f"Sex: {'Male' if sex == 1 else 'Female'}", f"Chest Pain Type: {cp}",
                    f"Resting BP: {trestbps}", f"Cholesterol: {chol}", f"Fasting Blood Sugar: {fbs}",
                    f"Resting ECG: {restecg}", f"Max Heart Rate: {thalach}", f"Exercise Induced Angina: {exang}",
                    f"ST Depression: {oldpeak}", f"Slope: {slope}", f"Vessels Colored: {ca}", f"Thal: {thal}"
                ]
                y = 670
                for item in patient_data:
                    c.setFont("Helvetica", 11)
                    c.drawString(60, y, item)
                    y -= 15
            
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y - 10, "Risk Factor Highlights:")
                y -= 30
                risk_factors = [
                    f"🔹 Age ({age}): {'High Risk' if age > 50 else 'Normal'}",
                    f"🔹 Cholesterol ({chol}): {'High' if chol > 240 else 'Normal'}",
                    f"🔹 Max HR ({thalach}): {'Low Fitness' if thalach < 100 else 'Healthy'}",
                    f"🔹 Oldpeak ({oldpeak}): {'Elevated' if oldpeak > 2.0 else 'Normal'}"
                ]
                for factor in risk_factors:
                    c.drawString(60, y, factor)
                    y -= 15
            
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y - 10, "Recommendations:")
                y -= 30
                recommendations = (
                    [
                        "🩺 Visit a cardiologist for further testing and treatment.",
                        "💊 Consider lifestyle changes, medication, and exercise.",
                        "🍽️ Monitor cholesterol and blood pressure regularly."
                    ] if prediction == 1 else [
                        "👍 Continue heart-healthy habits.",
                        "🥗 Eat a balanced diet, exercise regularly.",
                        "🧪 Periodic health screenings recommended."
                    ]
                )
                for tip in recommendations:
                    c.drawString(60, y, tip)
                    y -= 15
            
                c.setFont("Helvetica-Oblique", 9)
                c.drawString(50, 50, "This AI-based report should be reviewed by a medical professional.")
            
                c.save()
                buffer.seek(0)
            
                st.download_button(
                    label="📥 Download Heart Disease PDF Report",
                    data=buffer,
                    file_name="heart_disease_report.pdf",
                    mime="application/pdf"
                )

            st.markdown(f"""
            ### 🔍 Explanation:
            - **Chest Pain Type**: {cp}
            - **Cholesterol**: {chol} mg/dL
            - **Max Heart Rate**: {thalach} bpm
            - **Exercise Angina**: {exang}

            ### 📌 Next Steps:
            - ✅ Maintain a healthy diet and regular exercise if low-risk.
            - ⚠️ For high-risk, seek further tests like ECG, ECHO, and stress tests from a cardiologist.
            """)

    # -----------------------------
    # 🧠 Parkinson's Disease Prediction
    # -----------------------------
    elif selected == 'Parkinsons Disease Prediction':
        st.header("🧠 Parkinson's Disease Prediction")

        fields = [
            'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
            'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
            'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
            'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
            'spread1', 'spread2', 'D2', 'PPE'
        ]

        user_input = []
        cols = st.columns(3)
        for i, field in enumerate(fields):
            with cols[i % 3]:
                val = st.number_input(field, format="%.5f")
                user_input.append(val)

        if st.button("Predict Parkinson's Disease"):
            prediction = parkinsons_model.predict([user_input])[0]
            st.subheader("🧠 Prediction Result")
            if prediction == 1:
                st.error("The model predicts that this patient is likely to have **Parkinson’s Disease**.")
            else:
                st.success("The model predicts that this patient is unlikely to have **Parkinson’s Disease**.")
                
                

            st.markdown("""
            ### 🔍 Explanation:
            This prediction is based on voice measurements from clinical studies:
            - **Jitter/Shimmer**: Voice tremor levels
            - **HNR (Harmonics to Noise Ratio)**: Noise in vocal signal
            - **D2, Spread1**: Signal complexity measures related to neurological conditions

            ### 📌 Next Steps:
            - ✅ Continue regular monitoring if no risk.
            - ⚠️ If at risk, consult a neurologist and consider speech therapy and motor control evaluations.
            """)











# 🔴 Invalid Credentials
elif auth_status is False:
    st.error('Incorrect username or password')

# 🟡 Not Logged In Yet
elif auth_status is None:
    st.warning('Please enter your username and password')
