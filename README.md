🩺 Multiple Disease Prediction System
<div align="center"> <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python version"> <img src="https://img.shields.io/badge/Streamlit-1.30-green?logo=streamlit" alt="Streamlit version"> <img src="https://img.shields.io/badge/ML-Sklearn-orange?logo=scikit-learn" alt="Scikit-Learn"> <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Project Status"> </div>
<div align="center"> <img src="https://raw.githubusercontent.com/username/repo/main/demo.gif" alt="App Demo" width="800"> </div>
🌟 Introduction
The Multiple Disease Prediction System is an AI-powered healthcare application that predicts the likelihood of three critical diseases: Diabetes, Heart Disease, and Parkinson's Disease. Built with Python and Streamlit, this application combines machine learning models with an elegant user interface to provide instant risk assessments.

✨ Key Features
🔒 Secure Authentication System with encrypted credentials

🧠 Three specialized prediction models:

🩸 Diabetes Prediction (8 parameters)

❤️ Heart Disease Prediction (13 parameters)

🧠 Parkinson's Prediction (22 voice parameters)

📊 Detailed PDF Reports with risk analysis and recommendations

🌈 Modern UI with gradient backgrounds and animations

📱 Responsive Design works on all devices

🛠️ Technologies Used
Category	Technologies
Frontend	Streamlit, HTML/CSS
Backend	Python 3.8+
ML Frameworks	Scikit-Learn, Pickle
Authentication	Streamlit-Authenticator
PDF Generation	ReportLab
UI Components	Streamlit-Option-Menu
🚀 Getting Started
Prerequisites
Python 3.8 or higher

pip package manager

Installation
Clone the repository:

bash
git clone https://github.com/guptaprateek112/multiple-disease-prediction-using-ml.git
cd multiple-disease-prediction
Create a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Run the application:

bash
streamlit run app.py
Access the app in your browser at http://localhost:8501

🔑 Authentication
Use the following demo credentials to access the system:

Username: demo

Password: 123456789


🧠 Machine Learning Models
The application uses pre-trained models stored in pickle format:

Disease	Model File	Accuracy
Diabetes	models/diabetes_model.sav	86%
Heart Disease	models/heart_model.sav	89%
Parkinson's	models/parkinsons_model.sav	92%
Models were trained on publicly available datasets from Kaggle and UCI Machine Learning Repository.

🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request


Disclaimer: This application is for educational and demonstration purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

