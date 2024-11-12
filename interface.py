import gradio as gr
from app import *
from prompts import *
dropdown_options = ['Local','Huggingface API','OpenAI','Anthropic']
dropdown_options_api = ['','API key', 'Enviromental variable token']
default_keys = {'Local':'','Huggingface API':'HF_TOKEN','OpenAI':'OPENAI_API_KEY','Anthropic':'ANTHROPIC_API_KEY'}
api_key = ""
api_token=""


with gr.Blocks(fill_width=True,fill_height=True)as demo:

    with gr.Row(visible=True) as selection_interface:
        api_selection = gr.Dropdown(choices=dropdown_options, label="Select API", interactive=True)
        api_auth_dropdown= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True)
        api_value = gr.Textbox(label="Enter API key or enviromenatl variable name", interactive=True)
        api_key_button = gr.Button("Connect")
        api_auth_dropdown.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
        api_selection.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
    with gr.Row(visible=False) as main_interface:
        with gr.Column():
            chat_story = gr.ChatInterface(
            fn=Chat,
            chatbot=gr.Chatbot(height=600, value=[(None,initialize_story)]),
            additional_inputs=[api_selection,gr.Checkbox(label="Use ABCD options")])
        with gr.Column():
            change_api = gr.Button("Change API")
            image= gr.Image(label="Image",height=600,)
            image_button = gr.Button("Generate Image")

    image_button.click(fn=GenerateImage,inputs=chat_story.chatbot,outputs=image,api_name="generateImage")
    api_key_button.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value],outputs=[main_interface,selection_interface])
    change_api.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value],outputs=[selection_interface,main_interface])


demo.launch()
