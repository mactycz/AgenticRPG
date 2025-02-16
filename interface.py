import gradio as gr
from app import *
from prompts import *
from session import *
from common import *
from character import Character
from styles.css import css

with gr.Blocks(fill_width=True,fill_height=True,css=css)as demo:
    initialize_story_state = gr.State(initialize_story)
    current_session_name = gr.State("")
    session_id = gr.State("")
    image_state = gr.State({
                            "current_image_path":"helpers/placeholder.png",
                            "current_image_index":0,
                            "image_count":0
                            })
    session_type = gr.State("ABCD options")
                            
    with gr.Column() as selection_interface:
        with gr.Group():
            gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>LLM Settings</h4>")
            with gr.Row():
                api_selection_llm = gr.Dropdown(choices=dropdown_options_llm, label="Select API", interactive=True,value="Huggingface API")
                api_auth_dropdown_llm= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True,value="Enviromental variable token")
                api_key_value_llm = gr.Textbox(label=f"Enter auth key", interactive=True,value="HF_API_KEY")
            with gr.Row():
                llm_name= gr.Dropdown(label="Model name", interactive=True,allow_custom_value=True,value="meta-llama/Llama-3.1-8B-Instruct",choices=model_lists["Huggingface API"])
                provider_llm = gr.Textbox(label="provider",interactive=True)
                temperature = gr.Number(label="Temperature",interactive=True,value=0.7)
            

        with gr.Group():
            gr.Markdown("<h4 style='text-align: center; margin: 0; padding: 5px;'>Image model Settings</h4>")
            with gr.Row():
                api_selection_image = gr.Dropdown(choices=dropdown_options_image, label="Select API", interactive=True,value="Huggingface API")
                api_auth_dropdown_image= gr.Dropdown(choices=dropdown_options_api, label="Select auth method", interactive=True,value="Enviromental variable token")
                api_key_value_image = gr.Textbox(label=f"Enter auth key", interactive=True,value="HF_API_KEY")
            with gr.Row():
                model_name_image = gr.Textbox(label="Image model name", interactive=True,value="stabilityai/stable-diffusion-3.5-large-turbo")
                image_style = gr.Textbox(label="Image style",interactive=True)
                provider_image = gr.Textbox(label="provider",interactive=True)
        with gr.Group():
            with gr.Row(equal_height=True):
                session_type_list = gr.Dropdown(choices=session_types,interactive=True)
                new_session_button = gr.Button("New session",variant="primary",elem_id="new_session_button")
            
        with gr.Group():
            with gr.Row():
                saved_sessions = gr.Dropdown(
                    label="Saved Sessions",
                    choices=get_saved_sessions(),
                    allow_custom_value=False
                )
            with gr.Row():
                load_story_button = gr.Button("Load story", interactive=True)
        
        
    with gr.Column(visible=False) as main_interface:
        with gr.Row():
            with gr.Column():
                chat_story = gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(height=512,
                    value=[(None,initialize_story_state.value)]),
                    additional_inputs=[api_selection_llm,llm_name,temperature,
                        gr.Checkbox(label ="Automatically generate an image")])
                
            with gr.Column():
                change_api = gr.Button("Change API")
                image= gr.Image(image_state.value["current_image_path"],label="Image",height=512,type='filepath')
                with gr.Row():
                    previous = gr.Button("←")
                    counter = gr.Button(f"{image_state.value['current_image_index']}/{image_state.value['image_count']}")
                    next = gr.Button("→")
                image_button = gr.Button("Generate Image")

   
        with gr.Row():
            save_name = gr.Textbox(label="Story name",interactive=True,value="")
            save_option = gr.Dropdown(label="Save option",choices=["Full session","Session summary"],interactive=True)
            save_story_button = gr.Button("Save the story")

    api_auth_dropdown_llm.change(
        fn=update_placeholders_llm,
        inputs=[api_selection_llm,api_auth_dropdown_llm,gr.State(default_keys),gr.State(model_lists),gr.State(default_models_llm)],
        outputs=[api_key_value_llm,llm_name,llm_name])
    
    api_selection_llm.change(
        fn=update_placeholders_llm,
        inputs=[api_selection_llm,api_auth_dropdown_llm,gr.State(default_keys),gr.State(model_lists),gr.State(default_models_llm)],
        outputs=[api_key_value_llm,llm_name,llm_name])

    api_auth_dropdown_image.change(
        fn=update_placeholders_image,
        inputs=[api_selection_image,api_auth_dropdown_image,gr.State(default_keys),gr.State(default_models_image)],
        outputs=[api_key_value_image,model_name_image])
    
    api_selection_image.change(
        fn=update_placeholders_image,
        inputs=[api_selection_image,api_auth_dropdown_image,gr.State(default_keys),gr.State(default_models_image)]
        ,outputs=[api_key_value_image,model_name_image])

    load_story_button.click(
        fn=load_story,
        inputs=[saved_sessions],
        outputs=[initialize_story_state,chat_story.chatbot,session_id,image_state,session_type]
        ).then(
        fn=add_key_and_show_interface,
        inputs=[api_selection_llm, api_auth_dropdown_llm, api_key_value_llm, llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image],
        outputs=[main_interface,selection_interface])
    
    save_story_button.click(
        fn=summarize_and_save,
        inputs=[chat_story.chatbot,save_name,api_selection_llm,session_type,save_option,image_state,session_id],
        outputs=None)
    image_button.click(
        fn=generate_image,inputs=[chat_story.chatbot,api_selection_llm,api_selection_image,session_id,image_state,llm_name,model_name_image,temperature,image_style],
        outputs=[image,image_state])
    previous.click(
        fn = lambda ist, sid : update_image_state(ist,sid,"previous"),
        inputs=[image_state,session_id],
        outputs=image_state)

    next.click(
        fn = lambda ist, sid : update_image_state(ist,sid,"next"),
        inputs=[image_state,session_id],
        outputs=image_state)

    change_api.click(
        fn=add_key_and_show_interface,
        inputs=[api_selection_llm,api_auth_dropdown_llm,api_key_value_llm,llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image],
        outputs=[selection_interface,main_interface])
    
    new_session_button.click(
        fn=update_session_type,
        inputs=[session_type_list],
        outputs=session_type
    ).then(
        fn=add_key_and_show_interface,
        inputs=[api_selection_llm,api_auth_dropdown_llm,api_key_value_llm,llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image],
        outputs=[main_interface,selection_interface]
        ).then(fn = generate_session_id, outputs=session_id)
    
    chat_story.chatbot.change(
        fn=conditional_generate_image,
        inputs=[chat_story.chatbot, chat_story.additional_inputs[3],api_selection_llm,api_selection_image,session_id,image_state,llm_name,model_name_image,temperature,image_style],
        outputs=[image,image_state])
    
    image_state.change(
        fn=update_image,
        inputs=[image_state],
        outputs=[image,counter])


demo.launch()
