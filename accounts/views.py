import random
from threading import Thread
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework import permissions
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView


def create_otp():
    number_list = [x for x in range(1, 10)]  
    code_items_for_otp = []
    for i in range(4):
        num = random.choice(number_list)
        code_items_for_otp.append(num)
    otp_string = "".join(str(item)for item in code_items_for_otp)  
    return otp_string


@api_view(['POST'])
@permission_classes([])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # user.is_active = True

        # otp_string = create_otp()
        # email_subject = "Confirm Your Email"
        # email_body = render_to_string('confirm_email.html', {'OTP': otp_string})
        # email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        # email.attach_alternative(email_body, "text/html")
        # email.send()

        # user.otp = otp_string
        user.save()
        # wallet = Wallet.objects.create(user=user)
        # return Response({"message": "A confirmation email has been sent to your inbox."}, status=status.HTTP_201_CREATED)
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([])
def resend_otp(request):
    """Resend OTP to the user's email."""
    email = request.data.get('email')
    if not email:
        return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
        otp_string = create_otp()
        
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'OTP': otp_string})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()

        user.otp = otp_string
        user.save()
        return Response({"message": "A new OTP has been sent to your email."}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([])
def activate(request):
    """Activate user account using OTP."""
    email = request.data.get('email')
    otp = request.data.get('otp')
    try:
        user = CustomUser.objects.get(email=email)
        if user.otp == otp:
            user.is_active = True
            user.otp = None
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'email': user.email,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                "message": "Your account has been successfully activated!"
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([])
def login(request):
    # email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate( username=username,password=password)  #email=email,
    print("username:" ,username, "password", password) 
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            # 'email': user.email,
            'username': user.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([])
def custom_token_refresh(request):
    """Refresh access token using refresh token."""
    refresh_token = request.data.get("refresh_token")
    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        return Response({"access_token": str(token.access_token)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Blacklist the refresh token to log out the user."""
    refresh_token = request.data.get("refresh_token")
    print("refresh_token :--", refresh_token)
    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@permission_classes([])
def pass_reset_request(request):
    """Send OTP for password reset."""
    email = request.data.get("email")
    try:
        user = CustomUser.objects.get(email=email)
        if user.is_active:
            otp_string = create_otp()
            email_subject = "Password Reset Request"
            email_body = render_to_string('confirm_email.html', {'OTP': otp_string})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            Thread(target=email.send).start()

            user.otp = otp_string
            user.save()
            return Response({'message': 'A confirmation email has been sent to reset your password.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Your account is inactive. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'No user found with the provided email address.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([])
def reset_request_activate(request):
    email = request.data.get("email")
    otp = request.data.get('otp')
    try:
        user = CustomUser.objects.get(email=email)
        if user.is_active and user.otp == otp:
            user.otp = None
            user.save()
            return Response({"detail": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'No user found with the provided email address.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def reset_password(request):
    email = request.data.get("email")
    new_password = request.data.get('new_password')
    try:
        user = CustomUser.objects.get(email=email)
        if user.is_active:
            if user.check_password(new_password):
                return Response({'detail': 'New password cannot be the same as the old password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'detail': "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response({'detail': 'Your account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'No user found with the provided email address.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Profile updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'detail': 'Both old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'detail': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    if old_password == new_password:
        return Response({'detail': 'New password cannot be the same as the old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_user_details(request):  
#     username = request.data.get('username')
#     print(username)
#     if not username:
#         return Response({'detail': 'username is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         user = CustomUser.objects.get(username=username)
#         print(user)
#         user_details = {
#             "username": user.username,
#             "name": user.name,
#             "image": user.image.url if user.image else None,
#             "is_active": user.is_active,
#             "is_staff": user.is_staff,
#             "created_at": user.created_at,
#         }
#         return Response(user_details, status=status.HTTP_200_OK)
#     except CustomUser.DoesNotExist:
#         return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_details(request):  
    username = request.data.get('username', '').strip()  # Strip whitespace
    print(f"Received username: {username}")
    if not username:
        return Response({'detail': 'username is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Case-insensitive lookup
        user = CustomUser.objects.get(username__iexact=username)
        print(f"Found user: {user}")
        user_details = {
            "username": user.username,
            "name": user.name,
            "image": user.image.url if user.image else None,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "created_at": user.created_at,
        }
        return Response(user_details, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



# class view 
    
    
    
from django.core.mail import send_mail

class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=404)

        # Generate reset token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Construct reset URL
        reset_url = f"{settings.Base_URL}/reset-password/{uidb64}/{token}/"

        # Send email
        email_body = f"Hello {user.username},\n\nUse the link below to reset your password:\n{reset_url}"
        send_mail(
            subject="Password Reset",
            message=email_body,
            from_email="your-email@gmail.com",
            recipient_list=[email],
        )
        return Response({"message": "Password reset email sent."}, status=200)
    
    
class SetNewPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uidb64 or not token or not password:
            return Response({"error": "Missing required fields (uidb64, token, password)."}, status=400)

        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            # Validate the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid token."}, status=400)

            # Set the new password
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful."}, status=200)

        except Exception as e:
            return Response({"error": "An error occurred while resetting the password."}, status=400)
        
        
        
        
        