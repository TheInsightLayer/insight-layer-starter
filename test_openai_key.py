import openai
api_key = ""

client = openai.Client(api_key=openai.api_key)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.choices[0].message.content)