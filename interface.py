import gradio as gr
from app import *

dropdown_options = ['Local','Huggingface API','OpenAI','Anthropic']
api_key = ""
def add_key_and_show_interface(api_choice, provided_api_key):
    global api_key
    api_key = provided_api_key
    if provided_api_key:
        return gr.update(visible=True),gr.update(visible=False)
    return gr.update(visible=False),gr.update(visible=True)

with gr.Blocks(fill_width=True) as demo:

    with gr.Row(visible=True) as selection_interface:
        api_selection = gr.Dropdown(choices=dropdown_options, label="Select API", interactive=True)
        api_key_input = gr.Textbox(label="Enter API Key", placeholder="API Key", type="password", interactive=True)
        api_key_button = gr.Button("Add API Key",)
    with gr.Row(visible=False) as main_interface:
        with gr.Column():
            with gr.Row():
<<<<<<< HEAD
                UserStory = gr.Textbox(label="Story explaination",scale=3,)
=======
                user_story = gr.Textbox(label="Story explaination",scale=3,)
>>>>>>> master
                generate_story_button = gr.Button("Generate story")
            with gr.Row():
                story = gr.Textbox(label="Story",scale=3)
                characters = gr.Textbox(label="Characters",scale=3)
                image_prompt = gr.Textbox(label="Image prompt",scale=3)
                summary = gr.Textbox(label="Summary",scale=3)
            with gr.Row():
<<<<<<< HEAD
                UserStory = gr.Textbox(label="User input",scale=3,)
=======
                user_continuation = gr.Textbox(label="User input",scale=3,)
>>>>>>> master
                generate_continuation = gr.Button("Generate continuation")
        with gr.Column():
            change_api = gr.Button("Change API")
            image= gr.Image(label="Image",height=600,)
            image_button = gr.Button("Generate Image")

<<<<<<< HEAD
    generate_story_button.click(fn=hf.GenerateStory,inputs=UserStory,outputs=[story,characters,image_prompt,summary], api_name="generateStory")
    image_button.click(fn=hf.GenerateImage,inputs=image_prompt,outputs=image,api_name="generateImage")
    generate_continuation.click(fn=hf.GenerateContinuation,inputs =[summary,UserStory],outputs=[story,image_prompt,summary], api_name="generateContinuation")
=======
    generate_story_button.click(fn=hf.GenerateStory,inputs=user_story,outputs=[story,characters,image_prompt,summary], api_name="generateStory")
    image_button.click(fn=hf.GenerateImage,inputs=image_prompt,outputs=image,api_name="generateImage")
    generate_continuation.click(fn=hf.GenerateContinuation,inputs =[summary,user_continuation],outputs=[story,image_prompt,summary], api_name="generateContinuation")
>>>>>>> master
    api_key_button.click(fn=add_key_and_show_interface,inputs=[api_selection,api_key_input],outputs=[main_interface,selection_interface])
    change_api.click(fn=add_key_and_show_interface,inputs=[api_selection,api_key_input],outputs=[selection_interface,main_interface])

demo.launch()
