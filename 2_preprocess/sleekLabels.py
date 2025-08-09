import pandas as pd
import requests
import csv
import time

# 🔐 Azure GPT-4o configuration
API_KEY = "M2tMQ5DGXcyJNY45FQS8syNc9RdDtgSCjPic9Tdb0DYh6AVZCd93JQQJ99BGACHYHv6XJ3w3AAAAACOGpz6C"
DEPLOYMENT_NAME = "gpt-4o"  # e.g., "gpt4o-cyber-summarizer"
ENDPOINT = "https://shrav-mckii6fb-eastus2.cognitiveservices.azure.com/"
API_VERSION = "2024-03-01-preview"

# ✅ Summarization prompt builder
def build_prompt(verbose_text):
    return f"""
You are a cybersecurity assistant. Summarize the following verbose log analysis.

Extract only the essential details as mentioned below:
- Type of attack (e.g. credential theft, reconnaissance, lateral movement)
- The main technique or indicator behind this classification
Followed by a 1 line summary of the attack.

### Log Analysis:
{verbose_text}

### Response:
"""

# ✅ Send request to Azure GPT-4o
def summarize_with_gpt4o(text):
    full_prompt = build_prompt(text)

    url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a cybersecurity assistant."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.6,
        "top_p": 0.95
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"[ERROR] Could not summarize: {e}")
        return "Summary generation failed."

# ✅ Pipeline processor
def process_dataset(input_csv="all_attacks.csv", output_csv="sleekDataset2.csv"):
    df = pd.read_csv(input_csv)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["input_text", "sleek_summary"])  # Header

        for idx, row in df.iterrows():
            input_text = row["Logs"]
            verbose_analysis = row["Label"]

            print(f"🧠 Summarizing entry {idx+1}/{len(df)}...")
            summary = summarize_with_gpt4o(verbose_analysis)

            writer.writerow([input_text, summary])
            time.sleep(1.5)  # Throttle to respect API rate limits

    print(f"\n✅ sleekDataset.csv generated with {len(df)} rows.")

# ✅ Script runner
if __name__ == "__main__":
    process_dataset()