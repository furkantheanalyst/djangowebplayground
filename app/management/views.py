from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import ObtainTokenSerializer, MailAuthViewSerializer
from .authentication import JWTAuthentication
from .mailnotification import send_email
from users.models import MailAuth
from .generators import verification_code, verification_token, create_mail_auth, is_mailauth_valid

User = get_user_model()

class MailAuthView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MailAuthViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        vt=verification_token()
        vc=verification_code()
        create_mail_auth(username=username, temptoken=vt, verifycode=vc)

        user2=User.objects.get(username=username)
        send_email(user2.email, vc)
        return Response({'token': vt, 'res':'Verification code has been send your e-mail!'})

class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        vt = serializer.validated_data.get('verificationtoken')
        vc = serializer.validated_data.get('verificationcode')
        user=User.objects.get(username=username)

        mailauth = MailAuth.objects.filter(username=username).last()

        if is_mailauth_valid(mailauth, 9999) and mailauth and mailauth.temptoken == vt and mailauth.verifycode == vc and mailauth.username == username:
            jwt_token = JWTAuthentication.create_jwt(user)

            return Response({'access token': jwt_token})
        
        else:
            return Response ({'res':'Something went wrong!'}, status=status.HTTP_404_NOT_FOUND)

