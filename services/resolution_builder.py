import pandas as pd

from config.settings import VALID_SUPPORT_FLAGS


class ResolutionBuilder:

    def build_resolution(self, ticket_no, ack_groups):

        # ---------------- NORMALIZE TICKET ---------------- #

        ticket_id = str(ticket_no).split("-")[-1].strip()

        # ---------------- FAST LOOKUP ---------------- #

        rows = ack_groups.get(ticket_id)

        if rows is None or rows.empty:
            return ""

        # ---------------- SORT ---------------- #

        if "FDATE" in rows.columns:
            rows = rows.sort_values("FDATE")

        conversation = []

        for _, row in rows.iterrows():

            remark = str(row["REMARKS"]).strip()

            if remark == "" or remark.lower() == "nan":
                continue

            flag = str(row["FLAG"]).strip().upper()

            if flag in VALID_SUPPORT_FLAGS:
                role = "ADMIN"
            else:
                role = "USER"

            conversation.append(
                f"{role}: {remark}"
            )

        return "\n".join(conversation)