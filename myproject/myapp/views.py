# views.py
from rest_framework import viewsets
from .models import Card
from .serializers import CardSerializer

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import os
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView        

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate a verification token
        token = get_random_string(length=32)

        # Prepare the email content
        subject = 'Confirm your email address'
        message = f'Please confirm your email address by clicking the link: {request.build_absolute_uri(f"/api/confirm_email/{token}/")}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # Send the confirmation email
        send_mail(subject, message, from_email, recipient_list)

        return Response({
            'message': 'Registration successful. Please confirm your email address.',
            'token': str(RefreshToken.for_user(user))
        }, status=status.HTTP_201_CREATED)

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class ConfirmEmailView(generics.GenericAPIView):
    def get(self, request, token):
        # Logic for confirming email would go here
        # For example, update user status to 'confirmed'
        return Response({"message": "Email confirmed!"}, status=status.HTTP_200_OK)
    

class EmailLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)