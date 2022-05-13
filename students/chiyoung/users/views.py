import json, re

from django.views import View
from django.http import JsonResponse

from .models import Accounts


class SignupView(View):
    def post(self, request):
        
        try :
            signup_data = json.loads(request.body)

            # 이메일 유효성 검사        
            if "@" not in signup_data["email"] or "." not in signup_data["email"] :
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 400)

            # 비밀번호 유효성 검사
            if len(signup_data["password"]) < 8 :
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD : 비밀번호는 최소 8자리 이상'}, status = 400)
            if re.search('[a-zA-Z]+', signup_data["password"]) is None :
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD : 비밀번호는 최소 1개 이상의 문자 포함'}, status = 400)
            if re.search('[0-9]+', signup_data["password"]) is None :
               return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD : 비밀번호는 최소 1개 이상의 숫자 포함'}, status = 400)
            if re.search('[`~!@#$%^&*(),<.>/?]+', signup_data["password"]) is None :
               return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD : 비밀번호는 최소 1개 이상의 특수문자 포함'}, status = 400)
            
            account = Accounts.objects.create(
            name         = signup_data["name"],
            email        = signup_data["email"],
            password     = signup_data["password"],
            phone_number = signup_data["phone_number"],
            created_at   = signup_data["created_at"],
            updated_at   = signup_data["updated_at"],
        )
        except json.decoder.JSONDecodeError :
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        
        return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)