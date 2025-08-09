from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch
import pandas as pd

# 🔹 Path to your adapter folder
adapter_path = "C:/Users/shrav/Documents/LAST_REPORT/tinyLlama_correct/tinyllama_sleek"

# 🔍 Load PEFT config to get base model path
peft_config = PeftConfig.from_pretrained(adapter_path)
base_model_path = peft_config.base_model_name_or_path

# 🧠 Load base model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
base_model = AutoModelForCausalLM.from_pretrained(base_model_path)

# 🧩 Load LoRA adapter on top of base model
model = PeftModel.from_pretrained(base_model, adapter_path)

# 🛠️ Padding setup
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.eval()

# 🔍 Inference function
def generate_analysis(log):
    prompt = f"### Instruction:\nAnalyze the following Sysmon logs:\n{log}\n\n### Response:\n"
    encoding = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=924)
    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=4096,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=False
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded.replace(prompt, "").strip()

# 📁 Load logs and run inference
try:
    df = pd.read_csv("test_logs.csv")
    for i, row in df.iterrows():
        log = row['log_input']
        print(f"\n📝 Log {i+1}: {log}")
        print(f"📊 TinyLLaMA + LoRA Analysis:\n{generate_analysis(log)}")
except Exception as e:
    print(f"⚠️ Error loading CSV: {e}")