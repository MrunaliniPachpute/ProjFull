import os
import subprocess
import sys
import time

import streamlit as st

from config.settings import FAISS_INDEX, METADATA_FILE

st.set_page_config(
    page_title="Refresh Knowledge Base",
    page_icon="🔄",
    layout="wide"
)

# ---------------- HEADER ---------------- #

st.title("🔄 Refresh Knowledge Base")

st.markdown(
    """
    Rebuild the AI Knowledge Base whenever new complaints are resolved.

    This ensures the AI Assistant always searches the latest resolved tickets.
    """
)

st.divider()

# ---------------- INFO PANEL ---------------- #

st.info(
    """
### ⚙️ What happens during refresh?

- 📥 Load latest resolved complaints from Oracle
- 💬 Build conversations
- 🤖 Generate AI resolutions using Ollama
- 🔢 Generate embeddings
- 📚 Build FAISS Index
- 💾 Save Knowledge Base Metadata
"""
)

st.write("")

# ---------------- ACTION BUTTON ---------------- #

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    refresh_clicked = st.button(
        "🚀 Refresh Knowledge Base",
        use_container_width=True
    )

# ---------------- PROCESS ---------------- #

if refresh_clicked:

    with st.spinner("Refreshing Knowledge Base..."):

        start_time = time.time()

        try:

            result = subprocess.run(

                [
                    sys.executable,
                    "embedding.py"
                ],

                capture_output=True,
                text=True

            )

            elapsed = time.time() - start_time

            if result.returncode == 0:

                st.success(
                    f"✅ Knowledge Base Refreshed Successfully!\n\n"
                    f"⏱ Time Taken: {elapsed:.2f} seconds"
                )

                if result.stdout.strip():

                    with st.expander(
                        "📄 Process Output",
                        expanded=False
                    ):

                        st.code(result.stdout)

            else:

                st.error(
                    "❌ Knowledge Base Refresh Failed."
                )

                if result.stderr.strip():

                    with st.expander(
                        "⚠️ Error Details",
                        expanded=True
                    ):

                        st.code(result.stderr)

                if result.stdout.strip():

                    with st.expander(
                        "📄 Process Output"
                    ):

                        st.code(result.stdout)

        except Exception as e:

            st.error(
                f"Unexpected Error:\n\n{str(e)}"
            )

st.divider()

# ---------------- CACHE STATUS ---------------- #

st.subheader("🗂️ Current Cache Status")

col1, col2 = st.columns(2)

with col1:

    if os.path.exists(FAISS_INDEX):

        st.success("✅ FAISS Index Available")

    else:

        st.error("❌ FAISS Index Missing")

with col2:

    if os.path.exists(METADATA_FILE):

        st.success("✅ Knowledge Base Metadata Available")

    else:

        st.error("❌ Knowledge Base Metadata Missing")