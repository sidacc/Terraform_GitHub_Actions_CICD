import sys
import os
import json
from openai import AzureOpenAI

def main():
    # Read comment from file
    comment = open(sys.argv[1]).read()

    print("========== COMMENT RECEIVED ==========")
    print(comment)
    print("======================================")

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # Prompt to classify intent
    prompt = f"""
You are an AI DevOps ChatOps agent.

Analyze the GitHub comment below and decide the intent.

Allowed actions:
- deploy
- rollback
- analyze
- ignore

Rules:
- Deploy-related words → deploy
- Rollback / revert words → rollback
- Analyze / investigate → analyze
- Anything else → ignore

Respond ONLY in valid JSON:
{{ "action": "<value>" }}

Comment:
{comment}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    result = json.loads(response.choices[0].message.content)
    action = result["action"]

    # Write result for GitHub Actions
    with open("action.txt", "w") as f:
        f.write(action)

    print(f"AI ChatOps Decision: {action}")

if __name__ == "__main__":
    main()
