import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from users.models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 
            
            EMAIL_VALIDATION    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_VALIDATION = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&^])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            email    = data['email']
            password = data['password']
            
            if not re.match(EMAIL_VALIDATION, email): 
                return JsonResponse({'Message' : 'Invalid Email'}, status = 400)
            
            if not re.match(PASSWORD_VALIDATION, password): 
                return JsonResponse({'Message' : 'Invalid Password'},status = 400)

            if User.objects.filter(email = email).exists(): 
                return JsonResponse({'Message' : 'Email already in use'}, status = 400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
            User.objects.create(
                name         = data['name'],
                email        = email,
                password     = hashed_password,
                phone_number = data['phone_number'],
                )
            
            return JsonResponse({'Message': 'CREATED'}, status = 201)
        
        except KeyError: 
            return JsonResponse({'Message': 'KEY_ERROR'}, status = 400)
        
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 
            
            email    = data['email']
            password = data['password']
            
            user = User.objects.get(email = email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'Message': 'Invalid Password'}, status = 401)

            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({
                "message"      : "success",
                "access_token" : access_token
            }, status=200)
            
        except KeyError: 
            return JsonResponse({'Message': 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'Message': 'Invalid Email'}, status = 400)
        