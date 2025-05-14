from django.urls import path
from . import views
from django.conf import settings
from .views import RequestPasswordReset, SetNewPassword
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('token-refresh/', views.custom_token_refresh, name='token_refresh'),
    path('logout/', views.logout, name='logout'),
    path('update-profile/', views.update_user_profile, name='update_user_profile'),
    path('request-password-reset/', RequestPasswordReset.as_view(), name='request_password_reset'),
    path('set-new-password/', SetNewPassword.as_view(), name='set_new_password'),
    path('change-password/', views.change_user_password, name='change_user_password'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
    
    
    
    # path('resend-otp/', views.resend_otp, name='resend_otp'),
    # path('activate/', views.activate, name='activate'),
    # path('password-reset-request/', views.pass_reset_request, name='password_reset_request'),
    # path('reset-request-activate/', views.reset_request_activate, name='reset_request_activate'),
    # path('reset-password/', views.reset_password, name='reset_password'),
    path('delete-user/', views.delete_user, name='delete_user'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)