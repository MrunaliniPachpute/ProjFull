import streamlit as st

from services.semantic_search import SemanticSearch
from services.llm_service import LLMService

st.set_page_config(
    page_title="Query Assistance",
    layout="wide"
)

st.title("🔍 Query Assistance")

st.write("Search similar resolved complaints.")

subject = st.text_input("Subject")

complaint = st.text_area(
    "Complaint Description",
    height=150
)

# ---------------- SEARCH ---------------- #

if st.button("Search Similar Complaints", use_container_width=True):

    if subject.strip() == "" or complaint.strip() == "":

        st.warning("Please enter both Subject and Complaint.")
        st.stop()

    search = SemanticSearch()

    matches = search.search(subject, complaint)

    if len(matches) == 0:

        st.error("No suitable resolution found in database.")
        st.stop()

    best_match = matches[0]

    if best_match["similarity"] < 70:

        st.warning("No suitable resolution found in database.")
        st.stop()

    # Save current search
    st.session_state["best_match"] = best_match
    st.session_state["current_subject"] = complaint

    # Clear previous generated resolution
    st.session_state.pop("generated_resolution", None)

# ---------------- DISPLAY RESULT ---------------- #

if "best_match" in st.session_state:

    best_match = st.session_state["best_match"]

    st.success("Similar Complaint Found")

    st.markdown("---")

    c1, c2 = st.columns([5, 1])

    with c1:

        st.subheader(best_match["subject"])

    with c2:

        st.metric(
            "Similarity",
            f"{best_match['similarity']}%"
        )

    st.write("### Complaint")

    st.info(best_match["complaint"])

    with st.expander("Original Admin Conversation"):

        st.text_area(
            "",
            value=best_match["conversation"],
            height=180,
            disabled=True
        )

    st.markdown("---")

    if st.button(
        "🤖 Generate AI Resolution",
        use_container_width=True
    ):

        with st.spinner("Generating AI Resolution..."):

            llm = LLMService()

            resolution = llm.generate_resolution(
                best_match["subject"],
                st.session_state["current_subject"],
                best_match["conversation"]
            )
            print("="*50)
            print(resolution)
            print("="*50)

            st.session_state["generated_resolution"] = resolution

    if "generated_resolution" in st.session_state:

        st.write("### AI Suggested Resolution")

        st.text_area(
            "",
            value=st.session_state["generated_resolution"],
            height=220
        )