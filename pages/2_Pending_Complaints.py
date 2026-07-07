import streamlit as st

from services.database_service import DatabaseService
from services.semantic_search import SemanticSearch
from services.ticket_service import TicketService
from services.llm_service import LLMService

SIMILARITY_THRESHOLD = 70

st.set_page_config(
    page_title="Pending Complaints",
    layout="wide"
)

st.title("📝 Pending Complaints")

db = DatabaseService()
ticket_service = TicketService()
search = SemanticSearch()

pending = db.get_pending_complaints()

if pending.empty:
    st.success("No Pending Complaints Found.")
    st.stop()

st.write(f"Total Pending Complaints : {len(pending)}")

# ---------------- MAIN LOOP ---------------- #

for index, ticket in pending.iterrows():

    st.markdown("---")

    with st.expander(
        f"{ticket['TICKET_NO']} | {ticket['SUBJECT']}",
        expanded=False
    ):

        c1, c2 = st.columns(2)

        with c1:

            st.write("### Ticket Information")

            st.write(f"**Ticket No :** {ticket['TICKET_NO']}")
            st.write(f"**Status :** {ticket['STATUS_FLAG']}")
            st.write(f"**Priority :** {ticket['PRIOR_FLAG']}")
            st.write(f"**Department :** {ticket['ESTT_CODE']}")
            st.write(f"**System No :** {ticket['SYSTEM_NO']}")

        with c2:

            st.write("### Complaint")

            st.info(ticket["COMP_BRIEF"])

        # ---------------- SEARCH ---------------- #

        matches = search.search(
            ticket["SUBJECT"],
            ticket["COMP_BRIEF"],
            top_k=3
        )

        if len(matches) == 0:
            st.warning("No similar resolved complaint found.")
            continue

        options = [
            f"{i+1}. {row['subject']} ({row['similarity']}%)"
            for i, row in enumerate(matches)
        ]

        selected = st.selectbox(
            "Select Similar Complaint",
            options,
            key=f"select_{ticket['TICKET_NO']}"
        )

        selected_index = options.index(selected)
        selected_match = matches[selected_index]

        st.metric(
            "Similarity",
            f"{selected_match['similarity']}%"
        )

        st.write("### Similar Complaint")

        st.info(selected_match["complaint"])

        st.write("### Previous Conversation")

        st.text_area(
            "",
            value=selected_match["conversation"],
            height=220,
            disabled=True,
            key=f"conv_{ticket['TICKET_NO']}"
        )

        # ---------------- AI RESOLUTION ---------------- #

        resolution_key = (
            f"resolution_"
            f"{ticket['TICKET_NO']}_"
            f"{selected_index}"
        )

        if selected_match["similarity"] < SIMILARITY_THRESHOLD:

            st.warning(
                f"Best similarity is only {selected_match['similarity']}%."
            )

            st.info(
                "No reliable AI resolution can be suggested."
            )

        else:

            if st.button(
                "🤖 Generate AI Resolution",
                key=f"gen_{ticket['TICKET_NO']}_{selected_index}",
                use_container_width=True
            ):

                with st.spinner("Generating AI Resolution..."):

                    llm = LLMService()

                    resolution = llm.generate_resolution(

                        ticket["SUBJECT"],
                        ticket["COMP_BRIEF"],
                        selected_match["conversation"]

                    )

                    st.session_state[resolution_key] = resolution

                st.rerun()

            # ------------ SHOW ONLY AFTER GENERATION ---------------- #

            if resolution_key in st.session_state:

                resolution = st.text_area(

                    "Resolution To Approve",

                    value=st.session_state[resolution_key],

                    height=180,

                    key=f"text_{resolution_key}"

                )

                if st.button(

                    "✅ Approve Resolution",

                    key=f"approve_{ticket['TICKET_NO']}",

                    use_container_width=True

                ):

                    if resolution.strip() == "":

                        st.error("Resolution cannot be empty.")

                    else:

                        try:

                            ticket_service.approve_resolution(

                                ticket["TICKET_NO"],

                                resolution

                            )

                            st.success(
                                "Resolution Approved Successfully."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(str(e))