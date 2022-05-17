import json
import re
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from .models import User

from my_settings import SECRET_KEY, ALGORITHM
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
        try:
            input_data = json.loads(request.body)

            name         = input_data["name"]
            email        = input_data["email"]
            password     = input_data["password"]
            phone_number = input_data["phone_number"]

            EGEX_EMAILR = '[a-zA-Z0-9_-]+@[a-z]+.[a-z]+$'
            REGEX_PASSWORD = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[@#$%!^&+=]).*$'

            if not re.match(EGEX_EMAILR, email):
                return JsonResponse({"maessage":"이메일 형식에 @와 .이 포함되어있지않습니다"}, status=400)
 
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"입력해주신 비밀번호 형식에서 8자리이상 문자,숫자,특수문자가 포함되어야합니다"},status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"이미 회원가입된 이메일입니다."},status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode("UTF-8")

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    
# 로그인을 위한 View를 작성해야합니다. ****로그인 정보(이메일, 비밀번호)

# 로그인을 할 때는 사용자 계정과 비밀번호가 필수입니다.

# 계정이나 패스워드 키가 전달되지 않았을 경우, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.

# 계정을 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다.

# 비밀번호를 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다.

# 로그인이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.

class LoginView(View):
    def post(self,request):
        try:
            input_data = json.loads(request.body)

            email        = input_data["email"]
            password     = input_data["password"]

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "INVALID_USER"},status=401)

            user = User.objects.get(email=email)
            if not bcrypt.checkpw(password.encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"messange": "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse({"access_token": access_token}, status=200) 

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

            