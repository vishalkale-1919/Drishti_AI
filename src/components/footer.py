import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard, style_background_home


def footer_home():
    style_base_layout()
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    # st.markdown(f"""
    #         <div style="display:flex; align-items:center; justify-content:center; margin-top: 2rem; gap:6px;">
    #             <p style="font-weight:bold; color:white;">Created with ❤️ by </p>
    #             <img src='{logo_url}' alt='Apna College Logo' style="max-height:25px"/>
    #         </div>
    #             """, unsafe_allow_html=True)

def footer_dashboard():
    style_base_layout()
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    # st.markdown(f"""
    #         <div style="display:flex; align-items:center; justify-content:center; margin-top: 2rem; gap:6px;">
    #             <p style="font-weight:bold; color:black;">Created with ❤️ by </p>
    #             <img src='{logo_url}' alt='Apna College Logo' style="max-height:25px"/>
    #         </div>
    #             """, unsafe_allow_html=True)