import json
import re

from django.http import JsonResponse
from django.views import View

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            
            user_name          = user_data['user_name']
            user_email         = user_data["user_email"]
            password           = user_data["password"]
            phone_number       = user_data["phone_number"]
            regex_email        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            regex_phone_number = '^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$'
    
            if user_email == "" or password == "":
                return JsonResponse({"message":"이메일 또는 비밀번호를 입력해주세요"}, status=400)
                
            if not re.match(regex_email, user_email):
                return JsonResponse({"message":"이메일양식이 잘못되었습니다"}, status=400)

            if not re.match(regex_password, password):
                return JsonResponse({"message":"비밀번호는 8자리 이상, 문자, 숫자, 특수문자의 복합이어야합니다. "}, status=400)
            
            if not re.match(regex_phone_number, phone_number):
                return JsonResponse({"message":"핸드폰번호가 잘못되었습니다"}, status=400)

            email_check = User.objects.filter(user_email = user_email).exists()
            if not email_check :
                user = User(
                    user_name    = user_name,
                    user_email   = user_email,
                    password     = password,
                    phone_number = phone_number
                    )
                user.save()
                return JsonResponse({"message": "SUCCESS"}, status = 201)
            return  JsonResponse({"message":"이메일이 중복입니다"}, status=400)   
            
        except Exception as e:
            return JsonResponse({"message": e }, status = 500)    