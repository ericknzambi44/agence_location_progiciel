from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import account_activation_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not username or not email or not password:
        return Response({"error": "username, email et password requis"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Nom d'utilisateur déjà pris"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Cet email est déjà utilisé"}, status=400)

    user = User.objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name, last_name=last_name, is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    base_url = request.headers.get('Origin', 'http://localhost:8000')
    activation_link = f"{base_url}/api/auth/activate/{uid}/{token}/"

    send_mail(
        subject="Activez votre compte",
        message=f"Bonjour {username},\n\nCliquez sur le lien :\n{activation_link}\n\nMerci.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({"message": "Email de confirmation envoyé"}, status=201)

@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Compte activé. Vous pouvez vous connecter."})
    return Response({"error": "Lien invalide ou expiré"}, status=400)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            from django.contrib.auth import authenticate
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user and not user.is_active:
                return Response({"error": "Compte inactif. Activez-le via l'email."}, status=403)
        return response