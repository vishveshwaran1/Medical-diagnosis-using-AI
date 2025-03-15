import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import pymongo
import bcrypt
from datetime import datetime

# MongoDB Connection
def get_mongo_client():
    client = pymongo.MongoClient("YOUR_MONGODB_CONNECTION_STRING")  # Replace with your MongoDB connection string
    return client

# Initialize MongoDB
client = get_mongo_client()
db = client.disease_prediction_db  # Database name
users_collection = db.users  # Collection for users
results_collection = db.results  # Collection for storing user results

# Function to create a new user
def create_user(username, password):
    if users_collection.find_one({"username": username}):
        return False  # User already exists
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_data = {"username": username, "hashed_password": hashed_password}
    users_collection.insert_one(user_data)
    return True

# Function to verify user login
def verify_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["hashed_password"]):
        return True
    return False

# Function to save user results
def save_result(username, disease, result):
    result_data = {
        "username": username,
        "disease": disease,
        "result": result,
        "timestamp": datetime.now()
    }
    results_collection.insert_one(result_data)

# Function to fetch user results
def fetch_results(username):
    return list(results_collection.find({"username": username}))

# Change Name & Logo
st.set_page_config(page_title="Disease Prediction", page_icon="⚕️", layout="wide")

# Hiding Streamlit add-ons
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Adding Background Image
background_image_url = "https://static.vecteezy.com/system/resources/previews/000/235/537/original/vector-blue-medical-healthcare-background-with-cardiograph.jpg"  # Replace with your image URL

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url({background_image_url});
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stAppViewContainer"]::before {{
content: "";
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.7);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the saved models
models = {
    
    'diabetes': pickle.load(open('Models/diabetes_model.sav', 'rb')),
    'heart_disease': pickle.load(open('Models/heart_disease_model.sav', 'rb')),
    'parkinsons': pickle.load(open('Models/parkinsons_model.sav', 'rb')),
    'lung_cancer': pickle.load(open('Models/lungs_disease_model.sav', 'rb')),
    'thyroid': pickle.load(open('Models/Thyroid_model.sav', 'rb'))
}


# Login/Sign-In Page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login / Sign In 🔐")
    choice = st.radio("Select Option", ["Login", "Sign Up"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")

    elif choice == "Sign Up":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if create_user(username, password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists")

else:
    st.title(f"Welcome, {st.session_state.username}! 👋")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

    # Sidebar Navigation (Navbar)
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Prediction", "Lung Cancer Prediction", "Hypo-Thyroid Prediction", "My Results"],
            icons=["house", "activity", "heart-pulse", "person", "lungs", "capsule", "file-earmark-text"],
            menu_icon="cast",
            default_index=0,
        )

    # Home Page
    if selected == "Home":
        st.title("Welcome to Disease Prediction App 🏥")
        st.write("""
        This app predicts the likelihood of having certain diseases based on input parameters.
        Select a disease from the sidebar to get started.
        """)
        st.image("https://www.strategyand.pwc.com/m1/en/strategic-foresight/sector-strategies/healthcare/ai-powered-healthcare-solutions/img01-section1.jpg", use_container_width=True)
        st.write("""
        ### How to Use:
        1. **Select a Disease**: Choose the disease you want to predict from the sidebar.
        2. **Enter Details**: Fill in the required fields with the appropriate values.
        3. **Get Prediction**: Click on the test button to get the prediction result.
        """)

    # User Details Page (Past Results)
    elif selected == "My Results":
        st.title("My Results 📊")
        st.write("Here are your past results:")

        # Fetch user results from MongoDB
        results = fetch_results(st.session_state.username)
        if results:
            for result in results:
                with st.container():
                    st.write(f"**Disease:** {result['disease']}")
                    st.write(f"**Result:** {result['result']}")
                    st.write(f"**Date:** {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write("---")
        else:
            st.write("No past results found.")

    # Disease Prediction Pages
    elif selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction')
        st.write("Enter the following details to predict diabetes:")

        col1, col2 = st.columns(2)
        with col1:
            Pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20, step=1, help='Enter number of times pregnant')
            Glucose = st.number_input('Glucose Level', min_value=0, max_value=200, step=1, help='Enter glucose level')
            BloodPressure = st.number_input('Blood Pressure value', min_value=0, max_value=150, step=1, help='Enter blood pressure value')
            SkinThickness = st.number_input('Skin Thickness value', min_value=0, max_value=100, step=1, help='Enter skin thickness value')
        with col2:
            Insulin = st.number_input('Insulin Level', min_value=0, max_value=1000, step=1, help='Enter insulin level')
            BMI = st.number_input('BMI value', min_value=0.0, max_value=100.0, step=0.1, help='Enter Body Mass Index value')
            DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, max_value=2.5, step=0.01, help='Enter diabetes pedigree function value')
            Age = st.number_input('Age of the Person', min_value=0, max_value=120, step=1, help='Enter age of the person')

        if st.button('Diabetes Test Result'):
            diab_prediction = models['diabetes'].predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
            st.success(diab_diagnosis)
            save_result(st.session_state.username, "Diabetes", diab_diagnosis)

    # Add other disease prediction pages similarly...

    # Heart Disease Prediction Page
    elif selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction')
        st.write("Enter the following details to predict heart disease:")

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input('Age', min_value=0, max_value=120, step=1, help='Enter age of the person')
            sex = st.number_input('Sex (1 = male; 0 = female)', min_value=0, max_value=1, step=1, help='Enter sex of the person')
            cp = st.number_input('Chest Pain types (0, 1, 2, 3)', min_value=0, max_value=3, step=1, help='Enter chest pain type')
            trestbps = st.number_input('Resting Blood Pressure', min_value=0, max_value=200, step=1, help='Enter resting blood pressure')
            chol = st.number_input('Serum Cholesterol in mg/dl', min_value=0, max_value=600, step=1, help='Enter serum cholesterol')
            fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)', min_value=0, max_value=1, step=1, help='Enter fasting blood sugar')
            restecg = st.number_input('Resting Electrocardiographic results (0, 1, 2)', min_value=0, max_value=2, step=1, help='Enter resting ECG results')
        with col2:
            thalach = st.number_input('Maximum Heart Rate achieved', min_value=0, max_value=300, step=1, help='Enter maximum heart rate')
            exang = st.number_input('Exercise Induced Angina (1 = yes; 0 = no)', min_value=0, max_value=1, step=1, help='Enter exercise induced angina')
            oldpeak = st.number_input('ST depression induced by exercise', min_value=0.0, max_value=10.0, step=0.1, help='Enter ST depression value')
            slope = st.number_input('Slope of the peak exercise ST segment (0, 1, 2)', min_value=0, max_value=2, step=1, help='Enter slope value')
            ca = st.number_input('Major vessels colored by fluoroscopy (0-3)', min_value=0, max_value=3, step=1, help='Enter number of major vessels')
            thal = st.number_input('Thal (0 = normal; 1 = fixed defect; 2 = reversible defect)', min_value=0, max_value=2, step=1, help='Enter thal value')

        if st.button('Heart Disease Test Result'):
            heart_prediction = models['heart_disease'].predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            heart_diagnosis = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
            st.success(heart_diagnosis)

    # Parkinson's Prediction Page
    elif selected == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction")
        st.write("Enter the following details to predict Parkinson's disease:")

        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input('MDVP:Fo(Hz)', min_value=0.0, max_value=300.0, step=0.1, help='Enter MDVP:Fo(Hz) value')
            fhi = st.number_input('MDVP:Fhi(Hz)', min_value=0.0, max_value=300.0, step=0.1, help='Enter MDVP:Fhi(Hz) value')
            flo = st.number_input('MDVP:Flo(Hz)', min_value=0.0, max_value=300.0, step=0.1, help='Enter MDVP:Flo(Hz) value')
            Jitter_percent = st.number_input('MDVP:Jitter(%)', min_value=0.0, max_value=1.0, step=0.01, help='Enter MDVP:Jitter(%) value')
            Jitter_Abs = st.number_input('MDVP:Jitter(Abs)', min_value=0.0, max_value=0.1, step=0.001, help='Enter MDVP:Jitter(Abs) value')
            RAP = st.number_input('MDVP:RAP', min_value=0.0, max_value=0.1, step=0.001, help='Enter MDVP:RAP value')
            PPQ = st.number_input('MDVP:PPQ', min_value=0.0, max_value=0.1, step=0.001, help='Enter MDVP:PPQ value')
            DDP = st.number_input('Jitter:DDP', min_value=0.0, max_value=0.1, step=0.001, help='Enter Jitter:DDP value')
        with col2:
            Shimmer = st.number_input('MDVP:Shimmer', min_value=0.0, max_value=0.1, step=0.001, help='Enter MDVP:Shimmer value')
            Shimmer_dB = st.number_input('MDVP:Shimmer(dB)', min_value=0.0, max_value=10.0, step=0.1, help='Enter MDVP:Shimmer(dB) value')
            APQ3 = st.number_input('Shimmer:APQ3', min_value=0.0, max_value=0.1, step=0.001, help='Enter Shimmer:APQ3 value')
            APQ5 = st.number_input('Shimmer:APQ5', min_value=0.0, max_value=0.1, step=0.001, help='Enter Shimmer:APQ5 value')
            APQ = st.number_input('MDVP:APQ', min_value=0.0, max_value=0.1, step=0.001, help='Enter MDVP:APQ value')
            DDA = st.number_input('Shimmer:DDA', min_value=0.0, max_value=0.1, step=0.001, help='Enter Shimmer:DDA value')
            NHR = st.number_input('NHR', min_value=0.0, max_value=1.0, step=0.01, help='Enter NHR value')
            HNR = st.number_input('HNR', min_value=0.0, max_value=40.0, step=0.1, help='Enter HNR value')

        if st.button("Parkinson's Test Result"):
            parkinsons_prediction = models['parkinsons'].predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR]])
            parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
            st.success(parkinsons_diagnosis)

    # Lung Cancer Prediction Page
    elif selected == "Lung Cancer Prediction":
        st.title("Lung Cancer Prediction")
        st.write("Enter the following details to predict lung cancer:")

        col1, col2 = st.columns(2)
        with col1:
            GENDER = st.number_input('Gender (1 = Male; 0 = Female)', min_value=0, max_value=1, step=1, help='Enter gender of the person')
            AGE = st.number_input('Age', min_value=0, max_value=120, step=1, help='Enter age of the person')
            SMOKING = st.number_input('Smoking (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person smokes')
            YELLOW_FINGERS = st.number_input('Yellow Fingers (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person has yellow fingers')
            ANXIETY = st.number_input('Anxiety (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person has anxiety')
            PEER_PRESSURE = st.number_input('Peer Pressure (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person is under peer pressure')
            CHRONIC_DISEASE = st.number_input('Chronic Disease (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person has a chronic disease')
        with col2:
            FATIGUE = st.number_input('Fatigue (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person experiences fatigue')
            ALLERGY = st.number_input('Allergy (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person has allergies')
            WHEEZING = st.number_input('Wheezing (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person experiences wheezing')
            ALCOHOL_CONSUMING = st.number_input('Alcohol Consuming (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person consumes alcohol')
            COUGHING = st.number_input('Coughing (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person experiences coughing')
            SHORTNESS_OF_BREATH = st.number_input('Shortness Of Breath (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person experiences shortness of breath')
            SWALLOWING_DIFFICULTY = st.number_input('Swallowing Difficulty (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person has difficulty swallowing')
            CHEST_PAIN = st.number_input('Chest Pain (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person experiences chest pain')

        if st.button("Lung Cancer Test Result"):
            lungs_prediction = models['lung_cancer'].predict([[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]])
            lungs_diagnosis = "The person has lung cancer disease" if lungs_prediction[0] == 1 else "The person does not have lung cancer disease"
            st.success(lungs_diagnosis)

    # Hypo-Thyroid Prediction Page
    elif selected == "Hypo-Thyroid Prediction":
        st.title("Hypo-Thyroid Prediction")
        st.write("Enter the following details to predict hypo-thyroid disease:")

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input('Age', min_value=0, max_value=120, step=1, help='Enter age of the person')
            sex = st.number_input('Sex (1 = Male; 0 = Female)', min_value=0, max_value=1, step=1, help='Enter sex of the person')
            on_thyroxine = st.number_input('On Thyroxine (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if the person is on thyroxine')
            tsh = st.number_input('TSH Level', min_value=0.0, max_value=200.0, step=0.1, help='Enter TSH level')
        with col2:
            t3_measured = st.number_input('T3 Measured (1 = Yes; 0 = No)', min_value=0, max_value=1, step=1, help='Enter if T3 was measured')
            t3 = st.number_input('T3 Level', min_value=0.0, max_value=10.0, step=0.1, help='Enter T3 level')
            tt4 = st.number_input('TT4 Level', min_value=0.0, max_value=400.0, step=0.1, help='Enter TT4 level')

        if st.button("Thyroid Test Result"):
            thyroid_prediction = models['thyroid'].predict([[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]])
            thyroid_diagnosis = "The person has Hypo-Thyroid disease" if thyroid_prediction[0] == 1 else "The person does not have Hypo-Thyroid disease"
            st.success(thyroid_diagnosis)
