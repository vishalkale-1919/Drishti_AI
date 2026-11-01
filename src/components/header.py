import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard, style_background_home


def header_home():
    style_base_layout()
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;">
                <img src='{logo_url}' alt='DrishtiAI Logo' style="height:100px"/>
                <h1 style="text-align:center; color:#E0E3FF;">Drishti</br> AI</h1>
            </div>
                """, unsafe_allow_html=True)

def header_dashboard():
    style_background_dashboard()
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-top:30px;">
                <img src='{logo_url}' alt='DrishtiAI Logo' style="height:85px"/>
                <h1 style="text-align:left; color:#5865F2;">Drishti</br>AI</h1>
            </div>
                """, unsafe_allow_html=True)