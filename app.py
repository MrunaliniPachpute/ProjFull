import streamlit as st

st.set_page_config(
    page_title="Automated Complaint Resolution Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ DRDO Complaint Resolution Assistant")

st.markdown("---")

st.markdown("""
Welcome to the **Offline AI Complaint Resolution System**.

### Features

- 🔍 Semantic Complaint Search
- 🤖 Offline AI Resolution (Phi3)
- 🗄 Oracle Database Integration
- 📊 Complaint Dashboard
- 📄 Complaint Details
- 🔄 Refresh Knowledge Base

Use the **left sidebar** to navigate through different modules.
""")