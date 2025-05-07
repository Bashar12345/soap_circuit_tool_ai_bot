from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import Ai_botSerializer

from api.parts_recog.functions import process_image_and_text  # Import your function

class Ai_bot(APIView):
    def post(self, request):
        serializer = Ai_botSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        try:
            image_path = serializer.validated_data['image_path']
            question = serializer.validated_data['question']
            print(image_path, question)
            result = process_image_and_text(image_path, question)
            return Response({'result': result},status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)