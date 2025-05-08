import streamlit as st

st.set_page_config(
    page_title="SafeSpace Risk Dashboard",
    layout="wide",
)

st.title("🏠 Welcome to SafeSpace")

st.markdown("""
Welcome to the SafeSpace Financial Risk Dashboard!  
Use the sidebar to explore:
- 📊 Investment Simulator  
- 🤲 Loan Risk Assessment  
- 🎲 Investment Risk Assessment  
""")



# import streamlit as st

# # App Config
# st.set_page_config(page_title="SafeSpace Risk Dashboard", layout="wide")

# # Define the pages
# main_page = st.Page("investment_simulator.py", title="Investment Simulator", icon="📊")
# page_2 = st.Page("loan_assessment.py", title="Loan Risk Assessment", icon="🤲")
# page_3 = st.Page("risk_assessment.py", title="Investment Risk Assessment", icon="🎲")

# # Set up navigation
# pg = st.navigation([main_page, page_2, page_3])

# # Run the selected page
# pg.run()
