# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from g4f.client import Client
import json

@csrf_exempt
def get_interview_answer(request):
    if request.method == 'GET':
        question = request.GET.get('question', '')

        client = Client()

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
                            {question} 
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

        return JsonResponse({'answer': output})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
