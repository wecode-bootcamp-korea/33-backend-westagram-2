# python built-in module
import json
import re

# 외부 module
from django.http import JsonResponse
from django.views import View

# 내부 module
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
    
            User.objects.create(
                name         = data['name'],
                email        = email,
                password     = password,
                phone_number = data['phone_number'],
                )
            
            return JsonResponse({'Message': 'CREATED'}, status=201)
        
        except KeyError: 
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
        
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 
            
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email = email, password = password).exists():
                return JsonResponse({'Message': 'INVALID_USER'}, status=401)
            
            if User.objects.filter(email = email, password = password).exists():
                return JsonResponse({'Message': 'SUCCESS'}, status=200)
            
        except KeyError: 
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)