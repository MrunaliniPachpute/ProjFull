import pandas as pd

from services.resolution_builder import ResolutionBuilder
from services.llm_service import LLMService


class KnowledgeBase:

    def __init__(self):

        self.builder = ResolutionBuilder()
        # self.llm = LLMService()

    def build(self, complaints, acknowledgements):

        records = []

        resolved = complaints.copy()

        resolved = resolved[
            resolved["STATUS_FLAG"] == "R"
        ]

        resolved = resolved.drop_duplicates(
            subset="TICKET_NO"
        )
        acks = acknowledgements.copy()

        acks["ASNO"] = (
            acks["ASNO"]
            .astype(str)
            .str.strip()
        )

        acks["FLAG"] = (
            acks["FLAG"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        ack_groups = {
            ticket: group
            for ticket, group in acks.groupby("ASNO")
        }
        
        total = len(resolved)
        #for _, row in resolved.iterrows():

        for i, (_, row) in enumerate(resolved.iterrows(), start=1):
            if i % 100 == 0 or i == total:
                print(f"Processed {i}/{total} tickets...")
                
            ticket_no = str(row["TICKET_NO"]).strip()

            subject = str(
                row["SUBJECT"]
            ).strip()

            complaint = str(
                row["COMP_BRIEF"]
            ).strip()

            priority = str(
                row["PRIOR_FLAG"]
            ).strip()

            department = str(
                row["ESTT_CODE"]
            ).strip()

            status = str(
                row["STATUS_FLAG"]
            ).strip()

            conversation = self.builder.build_resolution(
                ticket_no,
                ack_groups
            )

            if conversation == "":
                continue

            # try:

            #     ai_resolution = self.llm.generate_resolution(
            #         subject,
            #         complaint,
            #         conversation
            #     )

            # except Exception:

            #     ai_resolution = ""

            # ai_resolution = str(
            #     ai_resolution
            # ).strip()

            # if ai_resolution == "":
            #     continue

            records.append({

                "ticket_no": ticket_no,
                "subject": subject,
                "complaint": complaint,
                "priority": priority,
                "department": department,
                "status": status,
                "conversation": conversation,
                # "ai_resolution": ai_resolution

            })

        kb = pd.DataFrame(records)

        if kb.empty:

            return pd.DataFrame(columns=[
                "ticket_no",
                "subject",
                "complaint",
                "priority",
                "department",
                "status",
                "conversation",
            ])

        kb = kb.drop_duplicates(
            subset="ticket_no"
        )

        kb = kb.reset_index(
            drop=True
        )

        return kb