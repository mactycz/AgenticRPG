import gradio as gr
from app import *
from prompts import *
dropdown_options = ['Local','Huggingface API','OpenAI','Anthropic']
dropdown_options_api = ['','API key', 'Enviromental variable token']
default_keys = {'Local':'','Huggingface API':'HF_TOKEN','OpenAI':'OPENAI_API_KEY','Anthropic':'ANTHROPIC_API_KEY'}
models_openai=[]
models_anthropic=[]
models_hf=[]
api_key = ""
api_token=""

with gr.Blocks(fill_width=True,fill_height=True)as demo:
    with gr.Column() as selection_interface:
        with gr.Group():
            gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>LLM Settings</h4>")
            with gr.Row():
                api_selection = gr.Dropdown(choices=dropdown_options, label="Select API", interactive=True,value="Huggingface API")
                api_auth_dropdown= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True,value="Enviromental variable token")
                api_value = gr.Textbox(label=f"Enter auth key", interactive=True,value="HF_TOKEN")
            with gr.Row():
                llm_name= gr.Textbox(label="Model name", interactive=True,value="meta-llama/Llama-3.3-70B-Instruct")
            

        with gr.Group():
            gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>Image model Settings</h4>")
            with gr.Row():
                api_selection_image = gr.Dropdown(choices=dropdown_options, label="Select API", interactive=True,value="Huggingface API")
                api_auth_dropdown_image= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True,value="Enviromental variable token")
                api_value_image = gr.Textbox(label=f"Enter auth key", interactive=True,value="HF_TOKEN")
            with gr.Row():
                image_model_name = gr.Textbox(label="Image model name", interactive=True,value="stabilityai/stable-diffusion-3.5-large-turbo")
                image_style = gr.Textbox(label="Image style",interactive=True)
        api_key_button = gr.Button("Connect")

        api_auth_dropdown.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
        api_selection.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
        


        
    with gr.Row(visible=False) as main_interface:
        with gr.Column():
            chat_story = gr.ChatInterface(
            fn=Chat,
            chatbot=gr.Chatbot(height=600,
                value=[(None,initialize_story)]),
                additional_inputs=[api_selection,
                    gr.Checkbox(label="Use ABCD options"),
                    gr.Checkbox(label ="Automatically generate an image")])
            
        with gr.Column():
            change_api = gr.Button("Change API")
            image= gr.Image(label="Image",height=600,)
            image_button = gr.Button("Generate Image")
    image_button.click(fn=GenerateImage,inputs=[chat_story.chatbot,image_style],outputs=image,api_name="generateImage")
    change_api.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value,llm_name,image_model_name],outputs=[selection_interface,main_interface])
    api_key_button.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value,llm_name,image_model_name],outputs=[main_interface,selection_interface])
    chat_story.chatbot.change(
        fn=conditional_generate_image,
        inputs=[chat_story.chatbot, chat_story.additional_inputs[2],image_style],
        outputs=image
)

demo.launch()
