dropdown_options_llm = ['Local','Huggingface API','OpenAI','Anthropic','OpenRouter']
dropdown_options_image = ['Local','Huggingface API','OpenAI']
dropdown_options_api = ['','API key', 'Enviromental variable token']
default_keys = {
    'Local':'',
    'Huggingface API':'HF_API_KEY',
    'OpenAI':'OPENAI_API_KEY',
    'Anthropic':'ANTHROPIC_API_KEY',
    'OpenRouter':'OPENROUTER_API_KEY'
}
models_openai=["gpt-4o","chatgpt-4o-latest","gpt-4o-mini","o1","o1-mini","o3-mini","o1-preview"]
models_anthropic=["claude-3-5-sonnet-latest","claude-3-5-haiku-latest","claude-3-opus-latest","claude-3-sonnet-20240229","claude-3-haiku-20240307"]
models_hf=[]
model_lists = {
    'Local':'',
    'Huggingface API':models_hf,
    'OpenAI':models_openai,
    'Anthropic':models_anthropic,
    'OpenRouter': models_hf
}
default_models_llm = {
    'Local':'',
    'Huggingface API':'meta-llama/Llama-3.1-8B-Instruct',
    'OpenAI':'gpt-4o',
    'Anthropic':'claude-3-5-sonnet-latest',
    'OpenRouter':'deepseek/deepseek-chat'
}
default_models_image = {
    'Local':'',
    'Huggingface API':'stabilityai/stable-diffusion-3.5-large-turbo',
    'OpenAI':'dall-e-3'
}
api_key = ""
api_token = ""