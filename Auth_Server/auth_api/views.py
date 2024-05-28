from django.shortcuts import render,redirect
# Create your views here.
from django.views import View
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from .authentication import EmailAuthBackend
from .serializers import CustomUserSerializer

from rest_framework import status, generics, renderers
from .models import CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView




############### Custom JWT Authentication Routes ################       

class RegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    

class CustomTokenRefreshView(TokenRefreshView):
    
     def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']

            # Decode the refresh token to obtain user information
            decoded_refresh = RefreshToken(refresh)
            user_id = decoded_refresh.payload.get('user_id')

            # Fetch the user instance from the database using the user_id
            user = CustomUser.objects.get(id=user_id)

            response_data = {
                'refresh': str(refresh),
                'access': str(access),
                'user': CustomUserSerializer(user).data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Customize error handling as needed

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data['refresh']
        access = response.data['access']
        response.data['user'] = CustomUserSerializer(self.user).data
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(access)
        return response

class EmailLoginView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
     

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class CustomLoginView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if '@' in username:
            user = EmailAuthBackend.authenticate(self, request, username=username, password=password)
        else:
            user = authenticate(username = username, password=password)
         
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            })
        
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





class AuthenticationPage(View):
    def get(self, request):
        return render(request, 'email/login.html')

    def post(self, request):
        if request.POST.get('action') == 'register':
            return self.handle_registration(request)
        else:
            return self.handle_login(request)

    def handle_registration(self, request):
        view = RegistrationView.as_view()
        response = view(request._request).render()
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('success_page')  # Redirect to a success page or login page
        return render(request, 'login.html', {'registration_errors': response.data})

    def handle_login(self, request):
        view = CustomLoginView.as_view()
        response = view(request._request).render()
        if response.status_code == status.HTTP_200_OK:
            return redirect('dashboard')  # Redirect to the dashboard or home page
        return render(request, 'login.html', {'login_errors': response.data})