from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.views.decorators.csrf import csrf_exempt
from .serializers import RegisterSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
def register_customer(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Registration successful!",
            "status":  True,
            "role":    user.role,
            "email":   user.email,
            "first_name": user.first_name,
            "tokens": {
                "access":  str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    return Response({
        "message": f"Welcome {request.user.first_name}",
        "role": request.user.role,
        "email": request.user.email
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['POST'])
def google_auth(request):
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )

        email          = id_info['email']
        first_name     = id_info.get('given_name', '')
        last_name      = id_info.get('family_name', '')
        profile_picture = id_info.get('picture', '')

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.first_name = first_name
            user.last_name = last_name
            user.registration_method = 'google'
            user.save()
        else:
            if user.registration_method != 'google':
                return Response({
                    'error': 'User registered with a different method',
                    'status': False
                }, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            "status": True
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid token', 'status': False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def google_auth(request):
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )

        email           = id_info['email']
        first_name      = id_info.get('given_name', '')
        last_name       = id_info.get('family_name', '')

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.first_name = first_name
            user.last_name  = last_name
            user.registration_method = 'google'
            user.save()
        else:
            if user.registration_method != 'google':
                return Response({
                    'error': 'User registered with a different method',
                    'status': False
                }, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "tokens": {
                "access":  str(refresh.access_token),
                "refresh": str(refresh)
            },
            "status":     True,
            "role":       user.role,        # ✅ role add
            "email":      user.email,       # ✅ email add
            "first_name": user.first_name,  # ✅ name add
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid token', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['POST'])
def google_auth(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        email      = id_info['email']
        first_name = id_info.get('given_name', '')
        last_name  = id_info.get('family_name', '')

        user, created = User.objects.get_or_create(email=email)

        if created:
            #New User
            user.first_name          = first_name
            user.last_name           = last_name
            user.registration_method = 'google'
            user.is_active           = True
            user.is_verified         = True
            user.save()
        else:
            #for login
            pass

        refresh = RefreshToken.for_user(user)
        return Response({
            "tokens":     {"access": str(refresh.access_token), "refresh": str(refresh)},
            "status":     True,
            "role":       user.role,
            "email":      user.email,
            "first_name": user.first_name,
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid token', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def home(request):
    return Response("Hello World")