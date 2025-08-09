import pandas as pd
import requests
from PreProcess import PreProcess

class SyntheticData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cleaned_text = ""
        self.response_text = ""

    def generate_cleaned_text(self):
        log_processor = PreProcess(self.file_path)
        log_processor.run_pipeline()
        self.cleaned_text = log_processor.cleaned_text

    def generate_response(self, api_key, endpoint, deployment_name):
        prompt_prefix = (
            "As a security analyst, you are presented with raw Windows Sysmon logs from a red team simulation."
            "Instructions: "
            "- Interpret each log as if investigating a potential compromise."
            "- Call out behaviors suggestive of lateral movement, execution from temporary directories, PowerShell abuse, file obfuscation, etc."
            "- Be assertive in flagging anything that seems out of place."
            "- Prioritize security over ambiguity—it's okay to over-classify in favor of catching threats."
            "List each entry as:"
            "- Summary"
            "- Suspicion Level: Benign / Suspicious / Malicious"
            "- Explanation"

            "Begin analysis below:"
        )
        full_prompt = prompt_prefix + self.cleaned_text
        
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        url = f"{endpoint}openai/deployments/{deployment_name}/chat/completions?api-version=2024-03-01-preview"
        payload = {
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.6,
            "top_p": 0.95
        }
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        print(response_json)
        self.response_text = response_json['choices'][0]['message']['content']

    def save_to_csv(self, output_path, append=False):
        import pandas as pd
        import os

        df = pd.DataFrame([{
            'input_text': self.cleaned_text,
            'copilot_response': self.response_text
        }])

        if append and os.path.exists(output_path):
            df.to_csv(output_path, mode='a', header=False, index=False)
        else:
            df.to_csv(output_path, index=False)
