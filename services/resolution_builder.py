import pandas as pd

from config.settings import VALID_SUPPORT_FLAGS


class ResolutionBuilder:

    def build_resolution(self, ticket_no, acknowledgements):

        # ---------------- NORMALIZE TICKET ---------------- #

        ticket_id = str(ticket_no).split("-")[-1].strip()

        rows = acknowledgements.copy()

        rows["ASNO"] = (
            rows["ASNO"]
            .astype(str)
            .str.strip()
        )

        rows["FLAG"] = (
            rows["FLAG"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # ---------------- FILTER TICKET ---------------- #

        rows = rows[
            rows["ASNO"] == ticket_id
        ]

        if rows.empty:
            return ""

        # ---------------- SORT ---------------- #

        if "FDATE" in rows.columns:
            rows = rows.sort_values("FDATE")

        conversation = []

        for _, row in rows.iterrows():

            remark = str(row["REMARKS"]).strip()

            if remark == "" or remark.lower() == "nan":
                continue

            flag = row["FLAG"]

            # ---------------- ROLE DETECTION ---------------- #

            if flag in VALID_SUPPORT_FLAGS:
                role = "ADMIN"

            else:
                role = "USER"

            conversation.append(
                f"{role}: {remark}"
            )

        return "\n".join(conversation)