import config
import openai

open_ai_key = config.OPEN_AI_API_KEY
openai.api_key = open_ai_key

model = "gpt-4o-mini"

query = "HBM 반도체에 대해서 설명해줘."

response = openai.chat.completions.create(
  model=model,
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": query}
  ]
)

print(response.choices[0].message.content)