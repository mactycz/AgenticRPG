import gradio as gr
from app import *
from prompts import *
dropdown_options = ['Local','Huggingface API','OpenAI','Anthropic']
dropdown_options_api = ['','API key', 'Enviromental variable token']
default_keys = {'Local':'','Huggingface API':'HF_TOKEN','OpenAI':'OPENAI_API_KEY','Anthropic':'ANTHROPIC_API_KEY'}
api_key = ""
api_token=""


with gr.Blocks(fill_width=True)as demo:

    with gr.Row(visible=True) as selection_interface:
        api_selection = gr.Dropdown(choices=dropdown_options, label="Select API", interactive=True)
        api_auth_dropdown= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True)
        api_value = gr.Textbox(label="Enter API key or enviromenatl variable name", interactive=True)
        api_key_button = gr.Button("Connect")
        api_auth_dropdown.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
        api_selection.change(fn=update_placeholders, inputs=[api_selection,api_auth_dropdown,gr.State(default_keys)],outputs=api_value)
    with gr.Row(visible=False) as main_interface:
        with gr.Column():
            with gr.Row():
                user_story = gr.Textbox(label="Story description",scale=3)
                with gr.Blocks():
                    with gr.Column():
                        generate_story_button = gr.Button("Generate story")
                        
            with gr.Row():
                story = gr.Textbox(label="Story",scale=3)
            with gr.Row():
                chat_story = gr.ChatInterface(
                fn=Chat,
                additional_inputs=gr.Checkbox(label="Use ABCD options"),
                chatbot=gr.Chatbot(height=300, value=[(None,initialize_story)])
        )


        with gr.Column():
            change_api = gr.Button("Change API")
            image= gr.Image(label="Image",height=600,)
            image_button = gr.Button("Generate Image")

    generate_story_button.click(fn=GenerateText,inputs=[gr.State(localPromptStory),user_story],outputs=story, api_name="generateStory")
    image_button.click(fn=GenerateImage,inputs=story,outputs=image,api_name="generateImage")
    #generate_continuation.click(fn=hf.GenerateText,inputs =[gr.State(localPromptStory),user_continuation,abcd],outputs=[story,image_prompt,summary], api_name="generateContinuation")
    api_key_button.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value],outputs=[main_interface,selection_interface])
    change_api.click(fn=add_key_and_show_interface,inputs=[api_selection,api_auth_dropdown,api_value],outputs=[selection_interface,main_interface])


demo.launch()
