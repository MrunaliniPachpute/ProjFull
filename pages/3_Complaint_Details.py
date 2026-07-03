import streamlit as st

from config.settings import VALID_SUPPORT_FLAGS
from services.database_service import DatabaseService

st.set_page_config(
    page_title="Complaint Details",
    layout="wide"
)

st.title("📄 Complaint Details")

db = DatabaseService()

ticket_no = st.text_input("Enter Ticket Number")

# ---------------- SEARCH ---------------- #

if st.button("Search Ticket", use_container_width=True):

    if ticket_no.strip() == "":
        st.warning("Please enter Ticket Number.")
        st.stop()

    complaint = db.get_ticket(ticket_no)

    if complaint.empty:
        st.error("Ticket Not Found.")
        st.stop()

    ticket = complaint.iloc[0]

    st.success("Ticket Found")

    st.markdown("---")

    # ---------------- TICKET INFO ---------------- #

    c1, c2 = st.columns(2)

    with c1:

        st.write("### 🧾 Ticket Information")

        st.write(f"**Ticket Number :** {ticket['TICKET_NO']}")
        st.write(f"**Subject :** {ticket['SUBJECT']}")
        st.write(f"**Status :** {ticket['STATUS_FLAG']}")
        st.write(f"**Priority :** {ticket['PRIOR_FLAG']}")
        st.write(f"**Department :** {ticket['ESTT_CODE']}")
        st.write(f"**System No :** {ticket['SYSTEM_NO']}")
        st.write(f"**Forwarded By :** {ticket['FED_ECODE']}")

    with c2:

        st.write("### 📅 Dates")

        st.write(f"**Complaint Date :** {ticket['FED_DATE']}")
        st.write(f"**Assigned Date :** {ticket['ASSIGN_DATE']}")
        st.write(f"**Resolved Date :** {ticket['RECT_DATE']}")
        st.write(f"**Assigned To :** {ticket['ASSIGN_TO']}")
        st.write(f"**Level :** {ticket['LEVEL_FLAG']}")

    st.markdown("---")

    # ---------------- COMPLAINT ---------------- #

    st.subheader("📝 Complaint Description")

    st.info(ticket["COMP_BRIEF"])

    st.markdown("---")

    # ---------------- CONVERSATION ---------------- #

    st.subheader("💬 Conversation")

    conversation = db.get_conversation(ticket_no)

    if conversation.empty:

        st.warning("No Conversation Available.")

    else:

        conversation = conversation.sort_values("FDATE")

        chat = []

        for _, row in conversation.iterrows():

            remark = str(row["REMARKS"]).strip()

            if remark == "" or remark.lower() == "nan":
                continue

            flag = str(row["FLAG"]).strip().upper()

            time = str(row["FDATE"])

            if flag in VALID_SUPPORT_FLAGS:

                role = "🛠 ADMIN"

            else:

                role = "👤 USER"

            chat.append(
                f"{role} [{time}]\n{remark}"
            )

        st.text_area(
            "Chat Conversation",
            value="\n\n".join(chat),
            height=500,
            disabled=True
        )