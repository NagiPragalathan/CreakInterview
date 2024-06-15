from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from g4f.client import Client

client = Client()

class ResponseQuestion(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'question', openapi.IN_QUERY, description="Question to be answered",
                type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={200: 'Answer generated successfully', 400: 'Invalid input'}
    )
    def get(self, request):
        try:
            question = request.query_params.get('question', '')
            print("working..!")
            if not question:
                return Response({"error": "Question parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
            
            messages = [
                {"role": "system", "content": "You are a useful AI to give the answer for given Question."},
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
                print(completion.choices[0].delta.content or "", end="", flush=True)
            return Response({"response": output}, status=status.HTTP_200_OK)
 
        except ValueError:
            return Response({"error": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)
