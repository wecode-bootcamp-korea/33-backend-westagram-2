import json
import re

from django.views import View
from django.http import JsonResponse

from .models import User
"""
1. 회원가입을 위한 View 를 작성해야합니다. 사용자 정보는 이름, 이메일, 비밀번호, 연락처(휴대폰), 그 외 개인정보를 포함한다.

2. 이메일이나 패스워드가 전달되지 않을 경우, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.

3. 이메일에는 @와 .이 필수로 포함되어야 합니다. 해당 조건이 만족되지 않은 경우 적절한 에러를 반환해주세요. 이 과정을 Email Validation이라고 합니다. 정규표현식을 활용해주세요. 

4. 비밀번호는 8자리 이상, 문자, 숫자, 특수문자의 복합이어야 합니다. 해당 조건이 만족되지 않은 경우, 적절한 에러를 반환해주세요. 이 과정을 Password Validation이라고 합니다. 정규표현식을 활용해주세요.

5. Email validation, Password Validation 과정에서 정규식을 사용해보세요.

6. 회원가입시 서로 다른 사람이 같은 이메일을 사용하지 않으므로 기존에 존재하는 자료와 중복되면 안됩니다. 적절한 에러를 반환해주세요.

7.회원가입이 성공하면 {"message": "SUCCESS"}, status code 201을 반환합니다.
"""
# Create your views here.

class SignupView(View):
    def post(self, request):
        input_data = json.loads(request.body)

        name         = input_data["name"]
        email        = input_data["email"]
        password     = input_data["password"]
        phone_number = input_data["phone_number"]

        email_check = '[a-zA-Z0-9_-]+@[a-z]+.[a-z]+$'
        password_check = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[@#$%^&+=]).*$'
        try: 
            if not re.match(email_check, email):
                return JsonResponse({"maessage":"이메일 형식에 @와 .이 포함되어있지않습니다"}, status=400)

            if not re.match(password_check, password):
                return JsonResponse({"message":"입력해주신 비밀번호 형식에서 8자리이상 문자,숫자,특수문자가 포함되어야합니다"},status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"이미 회원가입된 이메일입니다."},status=400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
 

