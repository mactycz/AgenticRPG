import gradio as gr
from interfaces.base_interface import BaseInterface
from prompts import *
import os
import datetime
class MainInterface(BaseInterface):
    def __init__(self, app_state, navigate_fn=None, tabs_component=None):
        super().__init__(app_state, navigate_fn, tabs_component)

    def build(self):
        with gr.Column() as self.container:
            with gr.Row():
                with gr.Column():
                    self.components["chat_story"] = gr.ChatInterface(
                        fn=self.chat,
                        chatbot=gr.Chatbot(
                            height=512,
                            value=[(None, self.app_state.initialize_story)]
                        ),
                        additional_inputs=[
                            gr.Checkbox(label="Automatically generate an image")
                        ]
                    )
                    
                    # # RPG interface
                    # self.components["true_rpg_interface"] = gr.Row(visible=False)
                    # with self.components["true_rpg_interface"]:
                    #     with gr.Column(min_width=300):
                    #         self.components["character_portrait_main"] = gr.Image(
                    #             "helpers/placeholder.png", 
                    #             interactive=False,
                    #             min_width=300
                    #         )
                    #     with gr.Column():
                    #         with gr.Column():
                    #             self.components["str_main"] = gr.Markdown("🗡 **Strength**: 18")
                    #             self.components["dex_main"] = gr.Markdown("🏹 **Dexterity**: 14")
                    #             self.components["int_main"] = gr.Markdown("📚 **Intelligence**: 16")
                    #             self.components["wis_main"] = gr.Markdown("🔮 **Wisdom**: 12")
                    #             self.components["con_main"] = gr.Markdown("❤️ **Constitution**: 15")
                    #             self.components["cha_main"] = gr.Markdown("🎭 **Charisma**: 10")
                    #         with gr.Column():
                    #             self.components["character_name_main"] = gr.Markdown("**Character Name**")
                    #             self.components["hp_main"] = gr.Markdown("**❤ 100/100**")
                    #             with gr.Row():
                    #                 self.components["roll_button"] = gr.Button("🎲")
                    #                 self.components["roll_results"] = gr.Markdown()

                with gr.Column():
                    self.components["image"] = gr.Image(
                        self.app_state.image_state["current_image_path"],
                        label="Image",
                        height=512,
                        type='filepath'
                    )
                    with gr.Row():
                        self.components["previous"] = gr.Button("←")
                        self.components["counter"] = gr.Button(
                            f"{self.app_state.image_state['current_image_index']}/"
                            f"{self.app_state.image_state['image_count']}"
                        )
                        self.components["next"] = gr.Button("→")
                    self.components["image_button"] = gr.Button("Generate Image")
    
                    with gr.Row():
                        self.components["save_name"] = gr.Textbox(
                            label="Story name",
                            interactive=True,
                            value=self.app_state.current_session_name or ""
                        )
                        self.components["save_option"] = gr.Dropdown(
                            label="Save option",
                            choices=["Full session"],
                            interactive=True
                        )
                        self.components["save_story_button"] = gr.Button("Save the story")
        
        return self.container
    
    def register_callbacks(self):
            def save_story_callback(chatbot, name, session_type, image_state):
                """Callback for saving a story session"""
                self.app_state.session_manager.set_session_data(name, chatbot, session_type, image_state)
                session_id = self.app_state.session_manager.save_session()
                
                self.app_state.current_session_id = session_id
                
                gr.Info(f"Story '{name}' saved successfully")
                
        
            self.components["save_story_button"].click(
                fn=save_story_callback,
                inputs=[
                    self.components["chat_story"].chatbot,
                    self.components["save_name"],
                    gr.State(lambda: self.app_state.session_type),
                    gr.State(lambda: self.app_state.image_state)
                ]
            )
            self.components["next"].click(
                fn=lambda: self.navigate_images("next"),
                outputs=[self.components["image"], self.components["counter"]]
            )
            
            self.components["previous"].click(
                fn=lambda: self.navigate_images("previous"),
                outputs=[self.components["image"], self.components["counter"]]
            )
            
            self.components["image_button"].click(
                fn=self.generate_image,
                outputs=[self.components["image"], self.components["counter"]]
            )

            self.components["chat_story"].chatbot.change(
                fn=self.conditional_generate_image,
                outputs=[self.components["image"], self.components["counter"]]
            )

    def navigate_images(self,direction):
        """Navigate through saved images"""
        if not self.app_state.image_state or "images" not in self.app_state.image_state:
            return None, ""
            
        current_index = self.app_state.image_state.get("current_image_index", 0)
        image_count = self.app_state.image_state.get("image_count", 0)
        
        if direction == "next" and current_index < image_count - 1:
            current_index += 1
        elif direction == "previous" and current_index > 0:
            current_index -= 1
            
        self.app_state.image_state["current_image_index"] = current_index
        self.app_state.image_state["current_image_path"] = self.app_state.image_state["images"][current_index]
        
        return (
            self.app_state.image_state["current_image_path"],
            f"{current_index + 1}/{image_count}"
        )


    def chat(self, message, history, auto_generate_image=False):
        """
        Process chat messages using the LLM model
        """
        self.app_state.auto_generate_image = auto_generate_image
        session_type = self.app_state.session_type
        if session_type != "True RPG":
            return self._handle_standard_chat(message, history)
        else:
            return self._handle_rpg_chat(message, history)
        
    def _handle_standard_chat(self, message, history):
        """Handle standard chat interaction (non-RPG)"""
        messages = []

        system_message = system_prompt + session_type_prompt[self.app_state.session_type] + self.app_state.character_backstory
        if self.app_state.llm.api_name != "Anthropic":
            messages.append({"role": "system", "content": system_message})
        
        if len(history) == 1:
            messages.append({"role": "assistant", "content": initialize_story})
            messages.append({"role": "user", "content": message})
            output = self.app_state.llm.generate(messages)
            history.append([None, messages[0]["content"] if len(messages) > 0 and "content" in messages[0] else ""])
            history.append([message, output])
        else:
            for user_msg, bot_msg in history:
                if user_msg is not None:
                    messages.append({"role": "user", "content": user_msg})
                if bot_msg is not None:
                    messages.append({"role": "assistant", "content": bot_msg})
            
            messages.append({"role": "user", "content": message})
            output = self.app_state.llm.generate(messages)
            
                
            history.append((message, output))
        
        self.app_state.story = history
        self.app_state.text_returned = True
        return output

    def _handle_rpg_chat(self, message, history):
        """Handle RPG chat interaction with game mechanics"""
        roll_needed=self.app_state.roll_needed
        messages = []
        llm=self.app_state.llm
        
        if llm.api_name != "Anthropic":
            messages.append({"role": "system", "content": llm.system_message})
        
        if len(history) == 1:
            messages.append({"role": "assistant", "content": initialize_story})
            messages.append({"role": "user", "content": message})
            
            output = llm.generate(messages)
            
            history.append([None, messages[0]["content"] if len(messages) > 0 and "content" in messages[0] else ""])
            history.append([message, output[:-1]]) 
            
            try:
                game_state_code = int(output[-1])
                match game_state_code:
                    case 1:  # player should continue the story
                        pass
                    case 2:  # player should roll
                        roll_needed = True
                        self.components["roll_button"].update(visible=True)
                    case 3:  # new character appears
                        print("new character appears")
                    case _:  # invalid option
                        pass
            except:
                print("Invalid game state code")
            
                
        else:
            for user_msg, bot_msg in history:
                if user_msg is not None:
                    messages.append({"role": "user", "content": user_msg})
                if bot_msg is not None:
                    messages.append({"role": "assistant", "content": bot_msg})
            
            messages.append({"role": "user", "content": message})
            output = llm.generate(messages)
            

            
        self.app_state.story = history
        self.app_state.text_returned = True
        return output[:-1] if self.app_state.session_type == "True RPG" else output

    def generate_image(self):
        image_model = self.app_state.image_model
        prompt = self.app_state.llm.generate([{"role": "user", "content": summarize_for_image + self.app_state.story[-1][1]}])
        if image_model.style != "":
            prompt = prompt + f' Generate the image in {self.app_state.image_model.style} style.'
        image = image_model.generate(prompt)
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        image_dir = f"sessions/{self.app_state.session_manager.session_id}/images"
        os.makedirs(image_dir, exist_ok=True)
        image_path = f"{image_dir}/image-{date}.png"
        image.save(image_path)
        
        # Update image state
        if "images" not in self.app_state.image_state:
            self.app_state.image_state["images"] = []
        
        self.app_state.image_state["images"].append(image_path)
        self.app_state.image_state["image_count"] = len(self.app_state.image_state["images"])
        self.app_state.image_state["current_image_index"] = self.app_state.image_state["image_count"] - 1
        self.app_state.image_state["current_image_path"] = image_path
        
        return image_path, f"{self.app_state.image_state['current_image_index'] + 1}/{self.app_state.image_state['image_count']}"
    
    def conditional_generate_image(self):
        if self.app_state.auto_generate_image and self.app_state.story and self.app_state.story[-1][1] is not None and self.app_state.text_returned:
            self.app_state.text_returned = False
            image,counter= self.generate_image()
            return image, counter
        else:
            return self.app_state.image_state["current_image_path"],f"{self.app_state.image_state['current_image_index'] + 1}/{self.app_state.image_state['image_count']}"

