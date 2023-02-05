import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = os.getenv('OPEN_AI_API_KEY')


def ask_chat_gpt(_source_loc, _dest_loc, _transit_method, _max_tokens=50, _model_engine="text-davinci-003"):
    prompt = "Can you give me step-by-step instructions to get from " \
             + _source_loc + " to " \
             + _dest_loc + " by " \
             + _transit_method

    # Generate a response
    completion = openai.Completion.create(
        engine=_model_engine,
        prompt=prompt,
        max_tokens=_max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Print the response
    return completion.choices[0].text

# if __name__ == '__chat_gpt__':
#     print('You executed test.py')
# else:
#     print("Something is not working")
# askChatGPT(_source_loc, _dest_loc, _transit_method, 50, "text-davinci-003")
