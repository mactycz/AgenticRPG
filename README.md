# AgenticRPG
This is an interactive RPG game based on agentic flow of transformer models.


# Process of making the app
Okay, this app has been created to test out agentic possibilities of models in storytelling, text generation, image generation, summarization, prompting etc.
At first the models supposed to be used locally, and then integration with API was supposed to be added, but for a quickstart due to the processing time and VRAM restraints it was done with huggingface api.
The pipeline at first was text generations with pipelines, but then after discovering agents in tranformers library it was changed to them to test it and learn something new.
Right now huggingface API works fine. OpenAI and Anthropic works great, for text generation. 
Huggingface API with image generation works, however it takes a long time and often models are too busy and don't return anything. That's why the option for automatic image generation doesn't work that well.
# TODO
- add image generation for OpenAI and local, as it currently works only for hf
- add character portrait
- implement RPG elements like stats, hp, rolling dices etc
- fix the models to generate options to choose from only if abcd option is selected
- add other non-standard APIs

# Image generated for the beginning of the story with model stabilityai/stable-diffusion-xl-base-1.0:
![alt text](helpers/RPG.png)

# Flow of the app
![alt text](helpers/Flow.drawio.png)