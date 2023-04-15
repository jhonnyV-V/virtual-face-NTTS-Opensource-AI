import os
import requests
from dotenv import load_dotenv
import json
from colorama import Fore, Back, Style
from utils.AI_Output_Input import *
from utils.ImageGenerator import *

# load values from the .env file if it exists
load_dotenv()

global language
language = 'English'

INSTRUCTIONS = f"""You are an helpful AI assistant of Ankit Yadav who is 14 years old boy who developed you.
Your Name is Friday. You are female.
Your reply should in {language} language only.
You should be so funny and humble.
You are powered by Yahkart and build by Ankit Yadav. 
If user request to play song or watch youtube or open website then you can open any website by just providing one link of request by appending "Source/Web: <and link of user request here>"  at the end of prompt.
You can generate, draw and create any image by generating the ultra real prompt for Stable Diffusion and append the prompt to generate image here "Source/generateImage: <add the prompt to generate image here> at the end of prompt and do it when user ask to draw or generate any image! YOU use stable diffusion to generate image."""

TEMPERATURE = 0.7
MAX_TOKENS = 200
MAX_CONTENT_LENGTH=2048
FREQUENCY_PENALTY = 0.6
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 50
LLM_URL = os.getenv("LLM_URL")


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    speakByPytts("Thinking...")

    payload = {
        "prompt": f"""### Instruction:{instructions}
        ### Prompt: {new_question}
        ### Response:
        """, 
        "max_context_length": MAX_CONTENT_LENGTH,
        "max_length": MAX_TOKENS if language == 'English' else 150,
        "max_new_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "top_k": 40,
        "top_p": 0.1,
        "do_sample": True,
        "typical_p": 1,
        "repetition_penalty": 1.18,
        "encoder_repetition_penalty": 1,
        "num_beams": 1,
        "penalty_alpha": 0,
        "min_length": 0,
        "length_penalty": 1,
        "no_repeat_ngram_size": 0,
        "early_stopping": True,
        "seed": -1,
    }

    response = requests.post(url=f'{LLM_URL}', json=payload).json()

    print(response)

    return response['results'][0]['text']

def main():
    # os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = takeCommand()
        if language == "english" and len(previous_questions_and_answers) == 0 and "friday" not in new_question.lower():
            pass
            
        else:
            if " " == new_question or len(new_question) == 0 or new_question == "None":
                    pass
            else:

                    response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

                    # add the new question and answer to the list of previous questions and answers
                    previous_questions_and_answers.append((new_question, response))

                    # print the response
                    print(Fore.GREEN + Style.BRIGHT + "Here you go: " + Style.NORMAL + Style.RESET_ALL + response)

                    global query
                    query = ''
                    
                    if 'Source/' in response:
                        query = response.split("Source/")[1]

                    response = response.split("Source/")[0]
                    speak(response)

                    if query and 'Web:' in query:
                        OpenWebsite(query.split("Web: ")[1])

                    if query and 'generateImage:' in query:
                        imagePrompt = query.split("generateImage: ")[1]
                        # OpenWebsite(generateImage(prompt=imagePrompt))
                        generateImageByStableDiffusion(imagePrompt)


if __name__ == "__main__":
    # voiceType('female')
    # voiceSpeed(170)
    SpeakingEnergy(500)
    # voiceType("Adam")
    # listeningLanguageChange('hi-In')
    # listeningLanguageChange('ne-NP')
    initializeAiVideoFun()
    main()