from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.parts_recog.functions import process_image_and_text  # Import your function

class Ai_bot(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            image_path = request.data.get('image_path')
            question = request.data.get('question')
            result = process_image_and_text(image_path, question)
            return Response({'result': result})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        



    