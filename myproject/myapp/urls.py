from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CardViewSet

router = DefaultRouter()
router.register(r'cards', CardViewSet)
from .views import SignupView,ConfirmEmailView
from .views import EmailLoginView

urlpatterns = [
    path('api/', include(router.urls)),
 path('api/signup/', SignupView.as_view(), name='signup'),
  path('api/confirm_email/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
   path('api/login/', EmailLoginView.as_view(), name='email_login'),
]
