import streamlit as st

from services.semantic_search import SemanticSearch

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

if st.button("Search Similar Complaints", width="stretch"):

    if subject.strip() == "" or complaint.strip() == "":

        st.warning("Please enter both Subject and Complaint.")
        st.stop()

    search = SemanticSearch()

    matches = search.search(subject, complaint)

    if len(matches) == 0:

        st.error("No suitable resolution found in database.")
        st.stop()

    best_match = matches[0]

    # ---------------- THRESHOLD CHECK ---------------- #

    if best_match["similarity"] < 70:

        st.warning("No suitable resolution found in database.")
        st.stop()

    st.success(f"{len(matches)} Similar Complaints Found")

    st.markdown("---")

    c1, c2 = st.columns([5, 1])

    with c1:

        st.subheader(best_match["subject"])

    with c2:

        st.metric("Similarity", f"{best_match['similarity']}%")

    st.write("**Complaint**")

    st.info(best_match["complaint"])

    with st.expander("Original Admin Conversation"):

        st.text_area(
            "",
            best_match["conversation"],
            height=180,
            disabled=True
        )

    st.write("### 🤖 Suggested Resolution")

    st.text_area(
        "",
        best_match["ai_resolution"],
        height=180,
        disabled=True
    )