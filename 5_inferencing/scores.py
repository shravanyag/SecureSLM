import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
from collections import Counter
import numpy as np

# 🔹 Load PEFT adapter and base model
adapter_path = "C:/Users/shrav/Documents/LAST_REPORT/tinyLlama_correct/tinyllama_sleek"
peft_config = PeftConfig.from_pretrained(adapter_path)
base_model_path = peft_config.base_model_name_or_path

tokenizer = AutoTokenizer.from_pretrained(base_model_path)
base_model = AutoModelForCausalLM.from_pretrained(base_model_path)
model = PeftModel.from_pretrained(base_model, adapter_path)

tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.eval()

# 🧠 CPU-only setup
device = torch.device("cpu")
model = model.to(device)

# 🔍 Inference wrapper
def generate_response(text):
    prompt = f"### Instruction:\nAnalyze the following Sysmon logs:\n{text}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=924).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=1024,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=False
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.replace(prompt, "").strip()

# ✅ Token-Level Evaluation
def evaluate_token_metrics(preds, targets):
    f1_scores, recall_scores = [], []

    for ref, pred in zip(targets, preds):
        ref_tokens = ref.split()
        pred_tokens = pred.split()

        ref_count = Counter(ref_tokens)
        pred_count = Counter(pred_tokens)

        overlap = sum((ref_count & pred_count).values())
        precision = overlap / len(pred_tokens) if pred_tokens else 0
        recall = overlap / len(ref_tokens) if ref_tokens else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

        f1_scores.append(f1)
        recall_scores.append(recall)

    print(f"\n🔍 Token-Level Evaluation Results")
    print(f"Token-Level F1     : {np.mean(f1_scores):.4f}")
    print(f"Token-Level Recall : {np.mean(recall_scores):.4f}")

# 📁 Load CSV and process top 50 samples
try:
    df = pd.read_csv("sleekLogs.csv")
    input_texts = df["input_text"].tolist()[:50]
    target_summaries = df["sleek_summary"].tolist()[:50]

    predictions = []
    for i, text in enumerate(input_texts):
        print(f"\n📝 Processing Log {i+1}")
        pred = generate_response(text)
        predictions.append(pred)
        print(f"📤 Prediction:\n{pred}")
        print(f"📌 Reference:\n{target_summaries[i]}")

    evaluate_token_metrics(predictions, target_summaries)

except Exception as e:
    print(f"⚠️ Error: {e}")