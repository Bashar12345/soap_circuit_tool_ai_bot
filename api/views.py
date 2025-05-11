from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import Ai_botSerializer
import os

from api.parts_recog.functions import process_image_and_text  # Import your function


from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from api.parts_recog.functions import process_image_and_text

class Ai_bot(APIView):
    def post(self, request):
        try:
            image_file = request.FILES.get('image')
            question = request.POST.get('question', '').strip() or "What is this component?"
            
            print("image from the frontend", image_file)
            print("question", question)

            if not request.session.session_key:
                request.session.create()
                request.session.save()
            user_id = request.session.session_key

            image_path = ''
            if image_file:
                media_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                os.makedirs(media_dir, exist_ok=True)
                image_path = os.path.join(media_dir, image_file.name)

                with open(image_path, 'wb+') as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)
                        
            print("image_path", image_path)

            result = process_image_and_text(image_path, question, user_id=user_id)
            return Response({'result': result}, status=200)

        except Exception as e:
            return Response({
                'error': 'Server error',
                'details': str(e)
            }, status=500)






# class Ai_bot(APIView):
#     def post(self, request):
#         serializer = Ai_botSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response({
#                 'error': 'Invalid input',
#                 'details': serializer.errors
#             }, status=400)
#         try:
#             image_path = serializer.validated_data.get('image_path', '')  # Default to empty string
#             question = serializer.validated_data['question']              # type: ignore
            
#             print("image", image_path)
#             print("question", question)
#             if not question.strip():
#                 question = "What is this component?"            
                
#             if not request.session.session_key:
#                 request.session.create()
#                 request.session.save()
#             user_id = request.session.session_key   # or 'anonymous'
            
#             result = process_image_and_text(image_path, question, user_id=user_id)
#             return Response({'result': result}, status=200)
#         except Exception as e:
#             return Response({
#                 'error': 'Server error',
#                 'details': str(e)
#             }, status=500)
            
            
            
# class Ai_bot(APIView):
#     def post(self, request):
#         try:
#             image_file = request.FILES.get('image_path')  # from multipart/form-data
#             question = request.POST.get('question', '').strip()

#             if not question:
#                 question = "What is this component?"

#             if not request.session.session_key:
#                 request.session.create()
#                 request.session.save()
#             user_id = request.session.session_key

#             # Save image to temp dir
#             image_path = ''
#             if image_file:
#                 temp_dir = 'tmp_uploads'
#                 os.makedirs(temp_dir, exist_ok=True)
#                 image_path = os.path.join(temp_dir, image_file.name)
#                 with open(image_path, 'wb+') as f:
#                     for chunk in image_file.chunks():
#                         f.write(chunk)

#             result = process_image_and_text(image_path, question, user_id=user_id)
#             return Response({'result': result}, status=200)

#         except Exception as e:
#             return Response({
#                 'error': 'Server error',
#                 'details': str(e)
#             }, status=500)




# from django.conf import settings
# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from api.parts_recog.functions import process_image_and_text

# class Ai_bot(APIView):
#     def post(self, request):
#         try:
#             image_file = request.FILES.get('image')
#             question = request.POST.get('question', '').strip() or "What is this component?"

#             if not request.session.session_key:
#                 request.session.create()
#                 request.session.save()
#             user_id = request.session.session_key

#             image_path = ''
#             if image_file:
#                 media_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#                 os.makedirs(media_dir, exist_ok=True)
#                 image_path = os.path.join(media_dir, image_file.name)

#                 with open(image_path, 'wb+') as f:
#                     for chunk in image_file.chunks():
#                         f.write(chunk)

#             result = process_image_and_text(image_path, question, user_id=user_id)
#             return Response({'result': result}, status=200)

#         except Exception as e:
#             return Response({
#                 'error': 'Server error',
#                 'details': str(e)
#             }, status=500)
