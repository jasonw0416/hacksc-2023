import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"


def ask_chat_gpt(_source_loc, _dest_loc, _transit_method, _max_tokens, _model_engine):
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
    print(completion.choices[0].text)

# askChatGPT(_source_loc, _dest_loc, _transit_method, 50, "text-davinci-003")
