import streamlit as st

st.set_page_config(
    page_title="SafeSpace Risk Dashboard",
    layout="wide",
)
# Get Firebase token from query params

token = st.query_params.get("token", [None])[0]

if token:
    st.session_state["idToken"] = token
else:
    st.error("🔒 You must be signed in to use the simulator.")
    st.stop()

st.title("SafeSpace Dashboard")

st.markdown("""
Welcome to the SafeSpace Financial Risk Dashboard!  
Use the sidebar to explore:
- 📊 Investment Simulator  
- 🤲 Loan Risk Assessment  
""")