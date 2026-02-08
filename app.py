import streamlit as st
from firebase_config import db

st.title("E-Commerce App")

try:
    # Try to read from Firestore 
    test = db.collection('users').limit(1).stream()
    st.success("Firebase connected successfully!")
except Exception as e:
    st.error(f"Firebase connection failed: {e}")