import streamlit as st
import numpy as np
import pickle as pkl

# ===============================
# Load Models
# ===============================
models = {
    "Logistic Regression": pkl.load(open("logistic.pkl", "rb")),
    "KNN": pkl.load(open("knn.pkl", "rb")),
    "Decision Tree": pkl.load(open("decision_tree.pkl", "rb")),
    "Naive Bayes": pkl.load(open("naive_bayes.pkl", "rb")),
    "SVM": pkl.load(open("svm.pkl", "rb")),
}

# ===============================
# Load Preprocessing
# ===============================
pt = pkl.load(open("power_transformer.pkl", "rb"))
scaler = pkl.load(open("robust_scaler.pkl", "rb"))

# ===============================
# Mappings
# ===============================
gender_map = {"Female": 0, "Male": 1}
platform_map = {
    "Instagram": 0,
    "Snapchat": 1,
    "Facebook": 2,
    "WhatsApp": 3,
    "TikTok": 4,
    "Twitter": 5,
    "YouTube": 6,
}

target_map = {0: "Healthy", 1: "At_Risk", 2: "Stressed"}

# ===============================
# UI
# ===============================
st.set_page_config(page_title="Mental Health Prediction", layout="centered")
st.title("🧠 Mental Health Prediction App")
st.markdown("Predict **Mental State** based on Social Media Behavior")

# ===============================
# Sidebar
# ===============================
st.sidebar.header("Model Selection")
model_name = st.sidebar.selectbox("Choose Model", list(models.keys()))
model = models[model_name]

# ===============================
# User Inputs (12 Feature)
# ===============================
st.subheader("User Information")

age = st.number_input("Age", 10, 100, 25)

gender = st.selectbox("Gender", list(gender_map.keys()))
platform = st.selectbox("Platform", list(platform_map.keys()))

daily_screen_time_min = st.slider("Daily Screen Time (minutes)", 0, 1440, 180)
social_media_time_min = st.slider("Social Media Time (minutes)", 0, 1440, 120)

negative_interactions_count = st.slider("Negative Interactions Count", 0, 500, 5)
positive_interactions_count = st.slider("Positive Interactions Count", 0, 500, 20)

sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
physical_activity_min = st.slider("Physical Activity (minutes/day)", 0, 300, 30)

anxiety_level = st.slider("Anxiety Level (0–10)", 0, 10, 3)
stress_level = st.slider("Stress Level (0–10)", 0, 10, 4)
mood_level = st.slider("Mood Level (0–10)", 0, 10, 6)

# ===============================
# Prediction
# ===============================
if st.button("Predict Mental State"):

    input_data = np.array([[
        age,
        gender_map[gender],
        platform_map[platform],
        daily_screen_time_min,
        social_media_time_min,
        negative_interactions_count,
        positive_interactions_count,
        sleep_hours,
        physical_activity_min,
        anxiety_level,
        stress_level,
        mood_level
    ]])

    # Preprocessing
    input_data = pt.transform(input_data)
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)[0]

    st.success(f"🧠 Mental State Prediction: **{target_map[prediction]}**")
