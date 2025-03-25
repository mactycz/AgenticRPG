import gradio as gr
from app import *
from prompts import *
from session import *
from common import *
from character import Character
from styles.css import css

with gr.Blocks(fill_width=True,fill_height=True,css=css)as demo:
    initialize_story_state = gr.State(initialize_story)
    true_rpg_interface = gr.State(true_rpg_interface)
    chat_height = gr.State(512)
    current_session_name = gr.State("")
    session_id = gr.State("")
    character_backstory = gr.State("")
    character_created = gr.State(False)
    image_state = gr.State({
                            "current_image_path":"helpers/placeholder.png",
                            "current_image_index":0,
                            "image_count":0
                            })
    
    session_type = gr.State("ABCD options")
                            
    with gr.Column(visible=True) as selection_interface:
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
                chatbot=gr.Chatbot(height=chat_height.value,
                    value=[(None,initialize_story_state.value)]),
                    additional_inputs=[character_backstory,api_selection_llm,llm_name,temperature,session_type,
                        gr.Checkbox(label ="Automatically generate an image")])
                
                with gr.Row(visible=False, elem_classes="character-card") as True_RPG_interface:
                    with gr.Column(min_width=300, elem_classes="identity-column"):
                        character_portrait_main =  gr.Image("helpers/placeholder.png", 
                                elem_classes="character-portrait",
                                interactive=False,
                                min_width=300)
                    with gr.Column(elem_classes="stats-column"):                        
                        with gr.Column(elem_classes="stats-grid"):
                            str_main=gr.Markdown("🗡 **Strength**: 18", elem_classes="stat-item")
                            dex_main=gr.Markdown("🏹 **Dexterity**: 14", elem_classes="stat-item")
                            int_main=gr.Markdown("📚 **Intelligence**: 16", elem_classes="stat-item")
                            wis_main=gr.Markdown("🔮 **Wisdom**: 12", elem_classes="stat-item")
                            con_main=gr.Markdown("❤️ **Constitution**: 15", elem_classes="stat-item")
                            cha_main=gr.Markdown("🎭 **Charisma**: 10", elem_classes="stat-item")
                        with gr.Column(elem_classes="name-container"):
                            character_name_main=gr.Markdown("**Character Name**", 
                                    elem_classes="name-text")
                            hp_main=gr.Markdown("**❤ 100/100**", 
                                    elem_classes="health-text")

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

    with gr.Column(visible=False) as character_creation_interface:
        with gr.Row():
            with gr.Column(scale=1):
                character_description = gr.Textbox(label="Character Description",interactive=True,lines=5)
                backstory = gr.Textbox(label="Backstory",interactive=True,lines = 5)
                generate_portrait = gr.Button("Generate Portrait")
            with gr.Column(scale=2):
                character_portrait = gr.Image(height=512,width=512)
                character_name = gr.Textbox(label="Character Name",interactive=True)
            with gr.Column(scale=1):
                str_stat = gr.Number(value=10,label="Strength")
                dex_stat = gr.Number(value=10,label="Dexterity")
                con_stat = gr.Number(value=10,label="Constitution")
                int_stat = gr.Number(value=10,label="Intelligence")
                wis_stat = gr.Number(value=10,label="Wisdom")
                cha_stat = gr.Number(value=10,label="Charisma")
                max_hp = gr.Number(value=100,label="Max HP")
        with gr.Row():
                begin_adventure = gr.Button("Begin Adventure!")



        



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
        inputs=[api_selection_llm, api_auth_dropdown_llm, api_key_value_llm, llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image,session_type,character_created],
        outputs=[main_interface,selection_interface,character_creation_interface])
    
    save_story_button.click(
        fn=summarize_and_save,
        inputs=[chat_story.chatbot,save_name,api_selection_llm,session_type,save_option,image_state,session_id],
        outputs=None)
    image_button.click(
        fn=generate_image,inputs=[gr.State(chat_story.chatbot.value[-1][-1]),api_selection_llm,api_selection_image,session_id,image_state,llm_name,model_name_image,temperature,image_style],
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
        inputs=[api_selection_llm,api_auth_dropdown_llm,api_key_value_llm,llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image,session_type,character_created],
        outputs=[selection_interface,main_interface,character_creation_interface])
    
    new_session_button.click(
        fn=update_session_type,
        inputs=[session_type_list],
        outputs=session_type
    ).then(
        fn=add_key_and_show_interface,
        inputs=[api_selection_llm,api_auth_dropdown_llm,api_key_value_llm,llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image,session_type,character_created],
        outputs=[main_interface,selection_interface,character_creation_interface]
        ).then(fn = generate_session_id, outputs=session_id)
    
    chat_story.chatbot.change(
        fn=conditional_generate_image,
        inputs=[chat_story.chatbot, chat_story.additional_inputs[3],api_selection_llm,api_selection_image,session_id,image_state,llm_name,model_name_image,temperature,image_style],
        outputs=[image,image_state])
    
    image_state.change(
        fn=update_image,
        inputs=[image_state],
        outputs=[image,counter])
    session_type.change(
        fn=update_interface_on_session_type,
        inputs=[session_type],
        outputs=[chat_story.chatbot,True_RPG_interface])
    
    begin_adventure.click(fn=lambda img: img,
           inputs=character_portrait,
           outputs=character_portrait_main
    ).then(
        fn=add_key_and_show_interface,
        inputs=[api_selection_llm,api_auth_dropdown_llm,api_key_value_llm,llm_name, provider_llm, api_selection_image, api_auth_dropdown_image, api_key_value_image, provider_image,session_type,character_created],
        outputs=[character_creation_interface,selection_interface,main_interface]
    ).then(fn=lambda x: True,
           inputs=character_created,
           outputs=character_created
    ).then(fn= lambda text: f"Main character backstory: {text}",
           inputs=[backstory],
           outputs=character_backstory
    ).then(fn=lambda name:name,
           inputs=character_name,
           outputs=character_name_main
    ).then(
    fn=lambda hp_state, s, d, i, w, co, ch: (
        hp_state, str(s), str(d), str(i), str(w), str(co), str(ch)),
    inputs=[gr.State(f"{max_hp.value}/{max_hp.value}"), str_stat, dex_stat, int_stat, wis_stat, con_stat, cha_stat],
    outputs=[hp_main, str_main, dex_main, int_main, wis_main, con_main, cha_main]
)
    

    generate_portrait.click(
        fn=lambda desc, backstory, *other_args: generate_image(
        f"Character description: {desc}\nCharacter background: {backstory}. Portrait.",
        *other_args),
        inputs=[character_description,backstory,api_selection_llm,api_selection_image,session_id,gr.State({}),llm_name,model_name_image,temperature,image_style],
        outputs=[character_portrait,gr.State({})]
    )


demo.launch()
