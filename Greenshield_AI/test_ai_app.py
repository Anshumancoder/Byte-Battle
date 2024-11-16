from groq import Groq

def draft_message(content, role = 'user'):
    return {
        "role": role,
        "content": content
    }

api_key = "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"

client = Groq(api_key=api_key)
messages = [
    {
        "role": "system",
        "content":"You are a helpful environmentalist assistant which can and should answer to queries through a broader perpective. Your mission is to inform the user about environmentalism and respond to their queries in the language of their prompt. If the user query does not have much to do with environmentalism then you should still be able to answer their query."
    }
]
print(messages)
prompt = input("Please enter your prompt: ")

messages.append(draft_message(prompt))

chat_completion = client.chat.completions.create(
    temperature = 1.0,
    n=1,
    model="mixtral-8x7b-32768",
    max_tokens = 10000,
    messages = messages
)
chat_completion.usage.total_tokens
print(chat_completion.choices[0].message.content)

