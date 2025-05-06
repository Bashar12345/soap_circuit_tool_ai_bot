from django.urls import path
from .views import RegisterUser, TestAuth
from .views import GenerateTemplateContent
from django.urls import path
from .views import RequestPasswordReset, SetNewPassword
from .views import GetImageUrl
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('register/', RegisterUser.as_view(), name='register'),
    # path('test-auth/', TestAuth.as_view(), name='test_auth'),
    # path('request-password-reset/', RequestPasswordReset.as_view(), name='request_password_reset'),
    # path('set-new-password/', SetNewPassword.as_view(), name='set_new_password'),
    

    path('generate-template/', GenerateTemplateContent.as_view(), name='generate_template'),
    path('get-image-url/', GetImageUrl.as_view(), name='get_image_url'),

    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)