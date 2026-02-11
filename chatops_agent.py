import sys
import os
from openai import AzureOpenAI

def main():
    comment = sys.argv[1]

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    prompt = f"""
You are an AI DevOps ChatOps controller.

User comment:
{comment}

Allowed commands:
- /deploy
- /rollback
- /status

If comment matches allowed command → respond with action.
If not → respond with ignore.

Respond ONLY with one word:
deploy
rollback
status
ignore
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    decision = response.choices[0].message.content.strip()

    print("AI Decision:", decision)

if __name__ == "__main__":
    main()
