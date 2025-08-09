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
def prompt_logs(verbose_text):
    return f"""
You're an expert cybersecurity analyst. Given the following Sysmon logs 
from an atomic red team simulation, identify exactly the **two most significant log entries** 
(copying their full original text) that indicate key adversary behaviors or suspicious activity. 
Do NOT summarize or interpret—just return the exact two log lines verbatim. Focus on entries 
related to credential dumping, execution lineage, or high-integrity post-exploitation activity.
### Logs:
{verbose_text}

### Response:
"""

# ✅ Send request to Azure GPT-4o
def summarize_logs(text):
    full_prompt = prompt_logs(text)

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

# ✅ Summarization prompt builder
def prompt_analysis(verbose_text):
    return f"""
Simplify the following cybersecurity log analysis into clear, direct text with no markdown, 
bullets, or formatting. Strip away headings, asterisks, and symbols. Retain all essential 
context about attack types, tools, and observed behaviors. Output should be in concise sentences 
suitable for training a language model. Avoid interpretation or new conclusions.
{verbose_text}

### Response:
"""

# ✅ Send request to Azure GPT-4o
def summarize_analysis(text):
    full_prompt = prompt_analysis(text)

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
def process_dataset(input_csv="test_logs.csv", output_csv="test_logs_new.csv"):
    df = pd.read_csv(input_csv)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["log_input"])  # Header

        for idx, row in df.iterrows():
            input_text = row["log_input"]
            #verbose_analysis = row["Label"]

            print(f"🧠 Summarizing entry {idx+1}/{len(df)}...")
            summary1 = summarize_logs(input_text)
            #summary2 = summarize_analysis(verbose_analysis)

            writer.writerow([summary1])
            time.sleep(1.5)  # Throttle to respect API rate limits

    print(f"\n✅ sleekDataset.csv generated with {len(df)} rows.")

# ✅ Script runner
if __name__ == "__main__":
    process_dataset()