local_prompt_story = f"Yoo are a game master and a narrator for an rpg session. Generate text for the story up to 500 words according to theme and user input. Treat it as a casual RPG seesion on friday night. Player should interact with the story."
summarize_for_image= "You are helpful and creative summarizer. You summarize story into one brieft prompt for image generation model.  You provide prompt only! Focus the most important aspect that could be visualized - a place, a character or an event. Make it visual and detailed up to 100 words. It should enrich the story."

initialize_story="Welcome to the RPG adventure! Describe the theme of the story, and I'll be a game master. "
summarize_for_future = "You are helpful and creative summarizer. You summarize the session, and it should include all of the important events and characters, and their characteristics. Make it as long as necessary, to include everything important. This summary should be useful for future sessions for continuation of the story."
session_type_prompt ={
    "ABDC options":"Generate 4 options for the player to choose from. Each option should be a possible action or a choice that the player can make. Make them different and interesting, but not too long.",
    "Text adventure":"Leave option for players to interact, but don't provide the options directly - players should provide their part of the story in form of full text dscription of their interaction.",
    "True RPG":""
}
true_rpg_action_required = """Based on the following interaction, decide what action is required for classic RPG DND style session. There are three options:
1. No action is required, continue the story as usual.
2. A roll is required to determine a success or failure of player action.
3. A new character appears in the story. It might be friend or a foe.
4. Something happens to the player or any character - it might be something good like stat upgrade or health restored - or something bad, like loosing health.
Output only the option number, formatted exactly as: (n), where n is 1, 2, 3, or 4. The output must be exactly 3 characters long. Do not include any additional text.
Example output:
(1)
"""

true_rpg_roll_need = """Based on the following interaction, decide what statistic the player needs to roll on in a classic RPG DND style.
Your answer should be in parenthesis. Arguments should be delimeted with comma. First argument should be True if roll is needed, False if not. 
Second argument should be statistic - one among these : Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma.
Third argument should be difficulty - between 1 and 30. 1-5 is incredibely easy, 6-10 is easy, 10-15 medium, 15-20 hard, over 20 is very hard, with 30 almost impossible. 10 should be dafault.
Example results:
(True,Charisma,15)
(False)
"""
true_rpg_output = """
Based on the classic RPG DND stat test result, continue the story and what happens next.
"""

true_rpg_character_creation = """ Provide a code that could be used for creating new character for classic RPG DND session.
Here is the character class initialization:
class Character():
    BASE_STATS = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    def __init__(self, name, max_hp, stats=None, current_hp=None)
Answer should be a valid code.
Do not return any more text than necessary.
Example result:
Lancelot = Character("Lancelot",20,stats = {"STR": 14, "DEX": 8, "CON": 13, "INT": 7, "WIS": 10, "CHA": 9})

"""

true_rpg_event_results="""

"""