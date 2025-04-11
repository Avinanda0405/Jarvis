from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)