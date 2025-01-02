from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
class LocalTransformersClient:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    def generate_response(self, messages):
        prompt = self.convert_messages_to_prompt(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_new_tokens=8000,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
    
    def convert_messages_to_prompt(self, messages):
        prompt = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        return prompt



class LocalLlamaClient:
    def __init__(self, model_path):
        from llama_cpp import Llama
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,
            n_ctx=30000,
        )
    
    def generate_response(self, messages):
        prompt = self.convert_messages_to_prompt(messages)
        response = self.llm(
            prompt,
            max_tokens=8000,
            temperature=0.7,
            stop=["User:", "System:"]
        )
        return response["choices"][0]["text"].strip()
    
    def convert_messages_to_prompt(self, messages):
        prompt = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        return prompt