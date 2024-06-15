from g4f.client import Client

client = Client()


Question="""
    sample question
"""


messages = [
    {"role": "system", "content": "You are a useful AI to give the answer for given Question."},
    {"role": "user", "content": "Hello"}
]
messages.append({
    "role": "user",
    "content": f""" NOTE: 
                    - The given Question is interview i need to answer for it. Give me the answer for Given Question.
                    - Don't give any other information, content, or any acknowledgment.
                    - Just give the corrected code only.
                    Question:
                    {Question} 
                """
})
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    max_tokens=600000,
    stream=True,
)

output = ""
for completion in response:
    try:
        output += completion.choices[0].delta.content or ""
    except AttributeError:
        pass
    print(completion.choices[0].delta.content or "", end="", flush=True)
    
    
print(output)