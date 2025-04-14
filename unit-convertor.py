import streamlit as st

st.set_page_config(page_title="Unit Converter", page_icon="📐")

# Header
st.markdown("""
    <div style='text-align:center;'>
        <h1 style='color:#EB5406;'>📐 Unit Converter App</h1>
        <p style='font-size:18px;'>Convert meters into centimeters easily!</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Input
meters = st.number_input("Enter value in meters", min_value=0)

# Button
if st.button("Enter"):
    centimeters = meters * 100
    st.success(f"✅ {meters} meters = {centimeters} centimeters")
