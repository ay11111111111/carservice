from ..models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import parsers, renderers, status
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.core.mail import send_mail, EmailMessage
from .others import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

@swagger_auto_schema(method='get')
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@swagger_auto_schema(operation_description="POST Register new user", method='post',
                    request_body=UserRegisterSerializer)
@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user'
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
            return Response(data)
        else:
            data = serializer.errors
            return Response(data, status = status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenAPI(ObtainAuthToken):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(operation_description="PUT Login", request_body=UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@swagger_auto_schema(methods=['PUT'], request_body=UserSerializer)
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def user_update(request):
    user = request.user

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['get', 'delete'])
@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def user_detail(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(operation_description="POST Register new user", method='post',
                    request_body=ProfileCreateSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def profile_create(request):
    if request.method == 'POST':
        user = request.user
        serializer = ProfileCreateSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user'
            data['name_surname'] = user.name_surname
            data['phone_number'] = user.phone_number
        else:
            data = serializer.errors

        return Response(data)



class NewPassword(GenericViewSet):
    serializer_class = NewPasswordSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="Change password",
                responses={400: 'Bad request body', 200:'Success'})
    def post(self, request):
        body = request.data.copy()
        serializer = self.serializer_class(data=body)
        if serializer.is_valid():
            if serializer.is_equal(body):
                if request.user.check_password(body['old_password']):
                    request.user.set_password(body['password'])
                    request.user.save()
                    return Response({'message':'Success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'passwords are not equal'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechSupportView(GenericViewSet):
    serializer_class = TechSupportSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="Tech Support",
                responses={400: 'Bad request body', 200:'Success'})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPassword(GenericViewSet):
    serializer_class = ForgotPasswordSerializer
    # permission_classes = (permissions.AllowAny, )

    def post(self, request):
        body = request.data.copy()
        serializer = self.serializer_class(data=body)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=body['email'])
                if user.is_active:
                    new_pass = randomStringDigits()
                    user.set_password(new_pass)
                    user.save()
                    subject = 'Сменить пароль!'
                    message = ''
                    from_mail = settings.EMAIL_HOST_USER
                    to_list = [user.email,]
                    current_site = get_current_site(request)
                    email_tmp = render_to_string(
                        'forgot_password.html',
                        {
                            'user': user,
                            'new_password': new_pass,
                        }
                    )
                    send_mail(subject, message, from_mail, to_list, fail_silently=True, html_message=email_tmp)
                    # msg = EmailMessage(subject, message, to_list)
                    # msg.send()
                    return Response({'message': 'Success'}, status=status.HTTP_200_OK)
                return Response({'message': 'Not active'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
