import ollama

from config.settings import OLLAMA_MODEL


class LLMService:

    def __init__(self):

        self.model = OLLAMA_MODEL

    def generate_resolution(self, subject, complaint, conversation):

        system_prompt = """You are an ERP Helpdesk Resolution Assistant. A previous support ticket has been retrieved using semantic search. Your job is to generate ONLY the recommended action that should be performed for a similar issue.
        Strict Rules:
            1. Use ONLY the information present in the conversation.
            2. Never use external knowledge.
            3. Never guess missing information.
            4. Never expand abbreviations or acronyms.
            5. Never invent commands, software names, or procedures.
            6. If an abbreviation appears (e.g., PH, SC, ERP), copy it exactly as written. Never expand or reinterpret it.
            7. Ignore greetings and acknowledgements.
            8. Extract ONLY the administrator's troubleshooting actions that directly resolved the issue. Ignore all user messages unless they provide essential context.
            9. Rewrite those actions as a recommendation for a support engineer.
            10. If multiple actions exist, combine them into one concise recommendation.
            11. Output exactly ONE sentence.
            12. No numbering.
            13. No markdown.
            14. No explanations.
            15. No prefixes like "Recommendation:".
            16. If no clear action exists, reply exactly: Recommendation not available. """

        user_prompt = f"""
Subject:
{subject}

Complaint:
{complaint}

Previous Resolved Conversation:
{conversation}
"""

        try:

            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={
                    "temperature": 0,
                    "top_p": 0.1,
                    "repeat_penalty": 1.15,
                    "num_predict": 160,
                    "seed":42,
                },
            )

            print("=" * 80)
            print(response["message"]["content"])
            print("=" * 80)

            answer = response["message"]["content"].strip()

            prefixes = [
                "Recommendation:",
                "Suggested Action:",
                "Recommended Action:",
                "Answer:",
            ]

            for prefix in prefixes:

                if answer.lower().startswith(prefix.lower()):

                    answer = answer[len(prefix) :].strip()

            answer = " ".join(answer.split())

            # if len(answer) > 120:

            #     answer = answer[:120].rstrip()

            if not answer or len(answer.strip()) == 0:
                return "Recommendation not available."

            return answer

        except Exception as e:
            print(f"Ollama Error: {e}")
            return "Recommendation not available."
