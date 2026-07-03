import streamlit as st
import pandas as pd
from datetime import datetime

from services.database_service import DatabaseService

st.set_page_config(
    page_title="Complaint Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ---------------- #

st.title("📊 Complaint Dashboard")

st.markdown(
    """
    Overview of all complaints including status distribution, SLA ageing,
    priority trends, and department-wise insights.
    """
)

st.divider()

db = DatabaseService()

complaints = db.get_all_complaints()

if complaints.empty:

    st.warning("No Complaint Data Found.")

    st.stop()

# ---------------- METRICS ---------------- #

total = len(complaints)

resolved = len(
    complaints[
        complaints["STATUS_FLAG"] == "R"
    ]
)

pending = len(
    complaints[
        complaints["STATUS_FLAG"] == "P"
    ]
)

initialized = len(
    complaints[
        complaints["STATUS_FLAG"] == "I"
    ]
)

st.subheader("📌 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📦 Total Complaints",
    total
)

c2.metric(
    "✅ Resolved",
    resolved
)

c3.metric(
    "⏳ Pending",
    pending
)

c4.metric(
    "🟡 Initialized",
    initialized
)

st.divider()

# ---------------- STATUS DISTRIBUTION ---------------- #

status_count = complaints[
    "STATUS_FLAG"
].value_counts()

st.subheader("📊 Complaint Status Distribution")

st.bar_chart(status_count)

st.divider()


status_count = complaints["STATUS_FLAG"].value_counts()

st.subheader("📊 Complaint Status Distribution")

# Convert to structured data
status_df = pd.DataFrame({
    "Status": ["Initialized (I)", "Pending (P)", "Resolved (R)"],
    "Count": [
        status_count.get("I", 0),
        status_count.get("P", 0),
        status_count.get("R", 0)
    ]
})

# ---------------- 2 COLUMN LAYOUT ---------------- #

c1, c2 = st.columns([1, 2])

with c1:
    st.metric("🟡 Initialized", status_df["Count"][0])
    st.metric("⏳ Pending", status_df["Count"][1])
    st.metric("✅ Resolved", status_df["Count"][2])

with c2:
    st.markdown("### 📊 Status Breakdown (Bar Chart with Colors)")

    st.bar_chart(
        status_df.set_index("Status")
    )

# ---------------- PIE CHART (WITH COLORS + LEGEND) ---------------- #

st.markdown("### 🥧 Status Distribution (Pie Chart)")

st.plotly_chart({
    "data": [{
        "labels": status_df["Status"],
        "values": status_df["Count"],
        "type": "pie",
        "marker": {
            "colors": ["#f1c40f", "#e67e22", "#2ecc71"]  # I, P, R colors
        },
        "textinfo": "label+percent",
        "hole": 0.4
    }],
    "layout": {
        "showlegend": True,
        "legend": {"orientation": "h"},
        "height": 400
    }
}, use_container_width=True)

# ---------------- SLA AGEING ---------------- #

st.subheader("⏱ SLA Ageing Analysis")


def calculate_age(date_string):

    try:

        fed_date = pd.to_datetime(date_string)

        return (datetime.now() - fed_date).days

    except:

        return 0


sla = complaints.copy()

sla["AGE_DAYS"] = sla["FED_DATE"].apply(calculate_age)


def sla_status(row):

    if row["STATUS_FLAG"] == "R":
        return "🟢 Normal"

    age = row["AGE_DAYS"]

    if age >= 15:
        return "🔴 Critical"

    elif age >= 7:
        return "🟡 Medium"

    else:
        return "🟢 Normal"


sla["SLA_STATUS"] = sla.apply(sla_status, axis=1)

sla = sla[
    [
        "TICKET_NO",
        "SUBJECT",
        "STATUS_FLAG",
        "AGE_DAYS",
        "SLA_STATUS"
    ]
]

st.dataframe(
    sla,
    use_container_width=True
)

st.divider()

# ---------------- PRIORITY ---------------- #

st.subheader("🔥 Priority Distribution")

priority = complaints[
    "PRIOR_FLAG"
].value_counts()

st.bar_chart(priority)

st.divider()

status_count = complaints["STATUS_FLAG"].value_counts()

st.subheader("📊 Complaint Status Distribution")

status_data = {
    "Initialized (I)": int(status_count.get("I", 0)),
    "Pending (P)": int(status_count.get("P", 0)),
    "Resolved (R)": int(status_count.get("R", 0)),
}

st.plotly_chart({
    "data": [{
        "labels": list(status_data.keys()),
        "values": list(status_data.values()),
        "type": "pie",
        "marker": {
            "colors": [
                "#f1c40f",  # I → Yellow
                "#e67e22",  # P → Orange
                "#2ecc71"   # R → Green
            ]
        },
        "textinfo": "label+percent",
        "hoverinfo": "label+value+percent",
        "hole": 0.45
    }],
    "layout": {
        "title": "Complaint Status Breakdown",
        "showlegend": True,
        "legend": {
            "orientation": "h"
        },
        "height": 450
    }
}, use_container_width=True)