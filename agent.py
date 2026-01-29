import sys
import os
import json
from openai import AzureOpenAI

def read_logs(file_path):
    with open(file_path, "r") as f:
        return f.read()

def main():
    test_log_file = sys.argv[1]
    logs = read_logs(test_log_file)

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    prompt = f"""
You are an AI DevOps agent.

Analyze the test logs below and decide ONE action.

Allowed decisions:
- proceed
- retry_tests
- block_pipeline

Rules:
- If logs show timeout or flaky errors → retry_tests
- If logs show consistent test failure → block_pipeline
- If no failures → proceed

Respond ONLY in valid JSON:
{{ "decision": "<value>" }}

Logs:
{logs}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    decision = json.loads(response.choices[0].message.content)["decision"]

    #  Write decision for GitHub Actions
    with open("decision.txt", "w") as f:
        f.write(decision)

    #  PRINT AI REASONING TO LOGS (IMPORTANT FOR LEARNING)
    print("========== AI ANALYSIS INPUT (TEST LOGS) ==========")
    print(logs)
    print("===================================================")
    print(f"AI Decision: {decision}")

if __name__ == "__main__":
    main()
