import os
import torch
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# --- Configuration ---
MODEL_ID = "madox81/SmolLM2-Cyber-Insight"


# --- LLM Class ---
class LLM:
    def __init__(self, model_id):
        print("Loading model...")
        
        # 1. Device & Dtype
        if torch.cuda.is_available():
            dtype = torch.float16
            device_map = "auto"
        else:
            dtype = torch.float32 # CPU stability
            device_map = "cpu"

        # 2. Load Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # 3. Load Base Model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            device_map=device_map
        )

        # # 4. Load LoRA Adapters
        # print(f"Loading adapters from {lora_id}...")
        # self.model = PeftModel.from_pretrained(
        #     self.model,
        #     lora_id,
        #     torch_dtype=dtype
        # )
        print("Model loaded!")

    def generate_resp(self, user_input, task_type):
        # CRITICAL: Use EXACT instructions from dataset generation
        if task_type == "MITRE Mapping":
            # Matches MITRE_INSTRUCTIONS[0] in your script
            instruction = "Map the following security event to MITRE ATT&CK tactics and techniques."
        elif task_type == "Severity Assessment":
            # Matches SEVERITY_INSTRUCTIONS[0] in your script
            instruction = "Assess the severity and business risk of the following incident."
        else:
            instruction = "Analyze the following:"

        # Format: "Instruction...\n\nInput: ..."
        formatted_message = f"{instruction}\n\nInput: {user_input.strip()}"

        messages = [{"role": "user", "content": formatted_message}]

        # Apply Chat Template
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            return_dict=True,
            return_tensors='pt',
            add_generation_prompt=True
        ).to(self.model.device)

        # Generation
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
                temperature=None,
                repetition_penalty=1.15,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        # Decode
        prompt_length = inputs['input_ids'].shape[1]
        generated_tokens = output[0][prompt_length:]
        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )

        return response.strip()

# --- Initialize ---
llm_instance = LLM(MODEL_ID)

# --- Gradio Interface ---
def process_input(user_input, task_type):
    return llm_instance.generate_resp(user_input, task_type)

with gr.Blocks(title="SmolLM2-Cyber-Insight") as demo:
    gr.Markdown("# 🛡️ SmolLM2-Cyber-Insight (Dual Task)")
    
    with gr.Row():
        with gr.Column(scale=2):
            task_selector = gr.Dropdown(
                label="Select Task Type",
                choices=["MITRE Mapping", "Severity Assessment"],
                value="MITRE Mapping"
            )
            
            input_box = gr.Textbox(
                label="Input Data",
                placeholder="Paste log, procedure, or incident description here...",
                lines=5
            )
            
            submit_btn = gr.Button("Analyze")
            output_box = gr.Textbox(label="Model Response (JSON)", lines=5)

    # Examples matching the new training data distribution
    gr.Markdown("### Examples")
    gr.Examples(
        examples=[
            # MITRE Example (Blue Team style)
            ["MITRE Mapping", "selection: CommandLine contains 'Invoke-Expression'"],
            # MITRE Example (Playbook style)
            ["MITRE Mapping", "Incident Type: Ransomware\nTarget: Finance Server"],
            # Severity Example
            ["Severity Assessment", "Incident: Ransomware affecting Finance Server."]
        ],
        inputs=[task_selector, input_box]
    )

    submit_btn.click(fn=process_input, inputs=[input_box, task_selector], outputs=output_box)

if __name__ == "__main__":
    demo.launch()