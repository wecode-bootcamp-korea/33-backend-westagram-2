import json, re, bcrypt, jwt
from django import views

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import User, FollowFollowing
from users.utils import token_reader


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

            user = User.objects.get(user_email = user_email)
                
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({'user_id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({
                "message": "success",
                "Token"  : access_token
            }, status=200) 

        except KeyError:
            return JsonResponse({"message": 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_EMAIL"}, status=401)

class FollowView(View):
    @token_reader
    def post(self, request, user_id):
        try:
            if not FollowFollowing.objects.filter(
                follow_user_id    = request.user.id,
                following_user_id = user_id
                ):
                FollowFollowing.objects.create(
                    follow_user_id    = request.user.id,
                    following_user_id = user_id,
                )
                return JsonResponse({'message':'팔로우가 되었습니다.'}, status=200)
            return  JsonResponse({'message':'언팔로우가 되었습니다.'}, status=200)   
        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status=401)   

    @token_reader
    def get(self, request, user_id):
        try:
            followings = FollowFollowing.objects.filter(follow_user_id = request.user)

            follow_count= followings.count()
            follow_list = [{
                    'user_id'   : following.following_user.id,
                    'user_name' : following.following_user.user_name,
                    'user_email': following.following_user.user_email,
                } for following in followings]

            return JsonResponse({
                'follow_count': follow_count,
                'follow_list' : follow_list
                }, status=200)
        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status=401)
