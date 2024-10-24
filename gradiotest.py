import random
import gradio as gr
from app import GenerateImage,GenerateStory,llm_engine, GenerateContinuation



def greet(name):
    return "Hello " + name + "!"

with gr.Blocks(fill_width=True) as demo:
    with gr.Row():
        with gr.Column():
            with gr.Row():
                generate_story_button = gr.Button("Generate story")
            with gr.Row():
                story = gr.Textbox(label="Story",scale=3)
                characters = gr.Textbox(label="Characters",scale=3)
                imageptompt = gr.Textbox(label="Image prompt",scale=3)
                summary = gr.Textbox(label="Summary",scale=3)
            with gr.Row():
                UserStory = gr.Textbox(label="User input",scale=3,)
                generate_continuation = gr.Button("Generate continuation")

        with gr.Column():
            image= gr.Image(label="Image",height=600,)
            image_button = gr.Button("Generate Image")
    generate_story_button.click(fn=GenerateStory, outputs=[story,characters,imageptompt,summary], api_name="generateStory")
    image_button.click(fn=GenerateImage,inputs=imageptompt,outputs=image,api_name="generateImage")
    generate_continuation.click(fn=GenerateContinuation,inputs =[summary,UserStory],outputs=[story,imageptompt,summary], api_name="generateContinuation")
demo.launch()
