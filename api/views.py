from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import Ai_botSerializer

from api.parts_recog.functions import process_image_and_text  # Import your function

class Ai_bot(APIView):
    def post(self, request):
        serializer = Ai_botSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Invalid input',
                'details': serializer.errors
            }, status=400)
        try:
            image_path = serializer.validated_data.get('image_path', '')  # Default to empty string
            question = serializer.validated_data['question']              # type: ignore
            if not question.strip():
                question = "What is this component?"            
                
            # Get user_id from session
            user_id = request.session.session_key or 'anonymous'
            
            # Process the request with or without image
            result = process_image_and_text(image_path, question, user_id=user_id)
            return Response({'result': result}, status=200)
        except Exception as e:
            return Response({
                'error': 'Server error',
                'details': str(e)
            }, status=500)