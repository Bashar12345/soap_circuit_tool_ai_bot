from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    # path('register/', RegisterUser.as_view(), name='register'),
    # path('test-auth/', TestAuth.as_view(), name='test_auth'),
    # path('request-password-reset/', RequestPasswordReset.as_view(), name='request_password_reset'),
    # path('set-new-password/', SetNewPassword.as_view(), name='set_new_password'),
    
    path('part-recog/', Ai_bot.as_view(), name='part_recog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)