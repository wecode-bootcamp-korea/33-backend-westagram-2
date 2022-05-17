import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            
            user_name          = user_data['user_name']
            user_email         = user_data["user_email"]
            password           = user_data["password"]
            phone_number       = user_data["phone_number"]
            REGEX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            REGEX_PHONE_NUMBER = '^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$'

            if not re.match(REGEX_EMAIL, user_email):
                return JsonResponse({"message":"이메일양식이 잘못되었습니다"}, status=400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"비밀번호는 8자리 이상, 문자, 숫자, 특수문자의 복합이어야합니다. "}, status=400)
            
            if not re.match(REGEX_PHONE_NUMBER, phone_number):
                return JsonResponse({"message":"핸드폰번호가 잘못되었습니다"}, status=400)

            if not User.objects.filter(user_email = user_email).exists():
                hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user = User(
                    user_name    = user_name,
                    user_email   = user_email,
                    password     = hash_password,
                    phone_number = phone_number
                    )
                user.save()
                return JsonResponse({"message": "SUCCESS"}, status = 201)
            return  JsonResponse({"message":"이메일이 중복입니다"}, status=400)   
            
        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status = 400)  

class LoginView(View):            
    def post(self, request):
        try:
            user_data = json.loads(request.body)

            user_email = user_data['user_email']
            password   = user_data['password']

            user = User.objects.filter(user_email = user_email)
            if not user.exists():
                return JsonResponse({"message": "이메일이 잘못되었습니다"}, status=401)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.get().password.encode('utf-8')):
                return JsonResponse({"message": "비밀번호가 틀렸습니다."}, status=401)

            encode_jwt = jwt.encode({'user_id':user.get().id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"Token": encode_jwt}, status=200) 

        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status = 400)