from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


def loadModel(model_name):
    torch.cuda.empty_cache()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    try:
        print(f'loading {model_name}')
        model = AutoModelForCausalLM.from_pretrained(model_name,device_map = 'cuda',low_cpu_mem_usage= True,use_safetensors=True,torch_dtype=torch.float16).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name,device_map = 'cuda')
        print(f'Model {model_name} loaded')
        return model, tokenizer
    except Exception as e:
        print(f'Error loading model: {e}')
        return None, None

def generate(model, tokenizer):
    
    response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1000)
    answer = response.choices[0].message.content
    return answer

def llm_engine(messages, client, stop_sequences=["Task"]) -> str:
    response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1000)
    answer = response.choices[0].message.content
    return answer