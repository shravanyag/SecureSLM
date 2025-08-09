from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import pandas as pd

# 🔹 Load model and tokenizer from fine-tuned folder
model_path = "C:/Users/shrav/Documents/LAST_REPORT/gpt2/fine_tuned_gpt2_sysmon/fine_tuned_gpt2_sysmon"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Configure tokenizer and model padding
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.eval()

# 🔍 Inference function with dynamic generation length
def generate_analysis(log):

    prompt = f"### Instruction:\nAnalyze the following Sysmon logs:\n{log}\n\n### Response:\n"

    encoding = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=924)
    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=1024,  # 924 input + 100 response
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=False
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded.replace(prompt, "").strip()

# 📁 Load logs from CSV and run inference
try:
    df = pd.read_csv("test_logs.csv")  # CSV with first column "log_input"
    for i, row in df.iterrows():
        log = row['log_input']
        print(f"\n📝 Log {i+1}: {log}")
        print(f"📊 GPT-2 Forensic Analysis:\n{generate_analysis(log)}")
except Exception as e:
    print(f"⚠️ Error loading CSV: {e}")
