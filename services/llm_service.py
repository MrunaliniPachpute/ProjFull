import ollama

from config.settings import OLLAMA_MODEL


class LLMService:

    def __init__(self):

        self.model = OLLAMA_MODEL

    def generate_resolution(self, subject, complaint, conversation):

        system_prompt = """
You are an experienced DRDO IT Helpdesk Engineer.

A previously resolved complaint is provided.

Your task is to generate a RECOMMENDED ACTION for resolving a NEW complaint that is similar.

Use ONLY the ADMIN actions present in the conversation.

Rules:
- Recommend what the support engineer should do.
- Do NOT summarize the old ticket.
- Do NOT describe what already happened.
- Do NOT mention the previous user.
- Do NOT say "issue resolved", "resolved successfully", or similar.
- Do NOT invent any actions/information not present in the conversation.
- Use action-oriented language such as:
  Repair...
  Reset...
  Restart...
  Reinstall...
  Update...
  Verify...
  Configure...
  Clear...
  Replace...
- If multiple actions were performed, combine them into one concise recommendation.
- Maximum 4 short sentences.
- One sentence only.
- No bullet points.
- No markdown.
- No prefixes.

If there is not enough information to recommend an action, reply exactly:

Recommendation not available.
"""

        user_prompt = f"""
Complaint:
{complaint}

Previous Resolved Conversation:
{conversation}
"""

        try:

            response = ollama.chat(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]

            )
            
            print("="*80)
            print(response["message"]["content"])
            print("="*80)

            answer = response["message"]["content"].strip()

            prefixes = [
                "Recommendation:",
                "Suggested Action:",
                "Recommended Action:",
                "Answer:"
            ]

            for prefix in prefixes:

                if answer.lower().startswith(prefix.lower()):

                    answer = answer[len(prefix):].strip()

            answer = " ".join(answer.split())

            # if len(answer) > 120:

            #     answer = answer[:120].rstrip()

            if answer == "":

                return "Recommendation not available."

            return answer

        except Exception as e:

            print(f"Ollama Error: {e}")

            return "Recommendation not available."