import openai
openai.api_key = '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'

messages = []
while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion
    answer = chat_response.choices[0].message.content
    print(f'ChatGPT: {answer}')
    messages.append({"role": "assistant", "content": answer})