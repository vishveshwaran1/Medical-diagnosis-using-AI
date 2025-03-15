# Disease Prediction App

![App Screenshot](https://via.placeholder.com/800x400.png?text=Disease+Prediction+App+Screenshot) <!-- Add a screenshot of your app here -->

## Overview
This is a **Streamlit-based web application** that predicts the likelihood of having certain diseases based on user-provided input parameters. The app uses machine learning models trained on various datasets to provide predictions for diseases such as diabetes, heart disease, Parkinson's disease, lung cancer, and thyroid conditions.

---

## Features
- **User Authentication**: Users can log in or sign up to access the app.
- **Disease Prediction**: Predict the likelihood of:
  - Diabetes
  - Heart Disease
  - Parkinson's Disease
  - Lung Cancer
  - Hypo-Thyroid
- **User Results**: View past prediction results stored in a MongoDB database.
- **Responsive UI**: Clean and user-friendly interface with a sidebar for navigation.

---

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: Scikit-learn
- **Database**: MongoDB
- **Libraries**:
  - `pymongo` for MongoDB interaction
  - `bcrypt` for password hashing
  - `pickle` or `joblib` for model serialization

---

## Installation

### Prerequisites
1. **Python**: Ensure Python 3.7 or higher is installed.
2. **MongoDB**: Set up a MongoDB database (local or cloud-based) and get the connection string.
3. **Dependencies**: Install the required Python libraries.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com//vishveshwaran1/Medical-diagnosis-using-AI
### Folder structure
disease-prediction-app/
├── app.py                  # Main Streamlit application
├── Models/                 # Folder containing trained models
│   ├── diabetes_model.sav
│   ├── heart_disease_model.sav
│   ├── parkinsons_model.sav
│   ├── lungs_disease_model.sav
│   └── Thyroid_model.sav
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
### Requirements
streamlit==1.26.0
pymongo==4.5.0
bcrypt==4.0.1
scikit-learn==1.2.2
pandas==2.0.3
numpy==1.24.3
joblib==1.3.2
pip install streamlit==1.26.0 && pip install pymongo==4.5.0 && pip install bcrypt==4.0.1 && pip install scikit-learn==1.2.2 && pip install pandas==2.0.3 && pip install numpy==1.24.3 && pip install joblib==1.3.2
