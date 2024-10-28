from loadModel import loadModel
from huggingface_hub import InferenceClient, login
import os
from transformers import CodeAgent
from PIL import Image
import uuid

token = os.environ.get('HF_TOKEN')

LLM = "mistralai/Mistral-7B-Instruct-v0.2"
ImageModel= "stabilityai/stable-diffusion-xl-base-1.0"
login(token)
clientLLM = InferenceClient(LLM)
clientImage = InferenceClient(ImageModel,)

def llm_engine(messages, stop_sequences=["Task"]) -> str:
    response = clientLLM.chat_completion(messages, stop=stop_sequences, max_tokens=1000,temperature=0.7)
    answer = response.choices[0].message.content
    return answer

def GenerateStory():
    random_token = str(uuid.uuid4())
    agent = CodeAgent(tools=[], llm_engine=llm_engine, add_base_tools=True,additional_authorized_imports=['json'])
    objects = agent.run(
        f"""Step 1: Generate text for a start for an rpg session in 500 words and add it to list that will be returned. Generate it as a Game Master and narrator and leave the option for the player to act and influence the story.
        Step 2: Generate 4 character sheets with a name, hp, mana, attack, armor and magic resist in form of valid json objects and add them to the return list.
        Step 3: Summarize the story into a detailed and very visual prompt for an image generation model and add it to return list.
        Step 4: Summarize the story into a briefer text that contain all important information of what happened.
        The code should be very simple and you should use only basic python libraries.
        Do not use web search.
        Return should contain: story, character sheet, prompt - objects[0] should be the story, objects[1] should be list of characters, objects[2] should be prompt for image generation, objects[3] should be summarization of the story so far and all important information that could be used for later .
        VERY IMPORTANT: Be extremely sure to provide correct code. 
        Random token to ignore {random_token}
        """,
        return_code=True)
    print(f"Agent results: {objects}")
    return objects


def GenerateImage(prompt):
    clientImage = InferenceClient("stabilityai/stable-diffusion-xl-base-1.0",)
    image = clientImage.text_to_image(prompt,num_inference_steps=50)
    image.save('RPG.png')
    return image

def GenerateContinuation(storySummary, UserInput):
    random_token = str(uuid.uuid4())
    agent = CodeAgent(tools=[], llm_engine=llm_engine, add_base_tools=True,additional_authorized_imports=['json'])
    objects = agent.run(
        f"""Step 1: Generate text for an rpg session in 500 words and add it to list that will be returned. Please base it on the story summary so far:
        {storySummary}
        And continue based on user input:
        {UserInput}
        Generate it as a Game Master and narrator and leave the option for the player to act and influence the story.
        Step 2: Summarize the story into a detailed and very visual prompt for an image generation model and add it to return list.
        Step 3: Summarize the story into a briefer text that contain all important information of what happened.
        The code should be very simple and you should use only basic python libraries.
        Do not use web search.
        Return should contain: story, character sheet, prompt - objects[0] should be the story, objects[1] should be list of characters, objects[2] should be prompt for image generation, objects[3] should be summarization of the story so far and all important information that could be used for later .
        VERY IMPORTANT: Be extremely sure to provide correct code. 
        Random token to ignore {random_token}
        """,
        return_code=True)
    print(f"Agent results: {objects}")
    return objects