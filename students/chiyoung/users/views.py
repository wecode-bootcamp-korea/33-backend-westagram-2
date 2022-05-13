import json

from django.views import View
from django.http import JsonResponse

from .models import Accounts


class SignupView(View):
    def post(self, request):
        
        try :
            signup_data = json.loads(request.body) # dictionary type
        # if Accounts.objects.filter(email=signup_data["email"]).exists():
        #         return JsonResponse({"message" : "Email address"}, status = 400)
        # else :
            account = Accounts.objects.create(
                name         = signup_data["name"],
                email        = signup_data["email"],
                password     = signup_data["password"],
                phone_number = signup_data["phone_number"],
                created_at   = signup_data["created_at"],
                updated_at   = signup_data["updated_at"],
            )
        except json.decoder.JSONDecodeError :
            return JsonResponse({'MESSAGE' : '이건 Json decode error 발생 케이스'}, status = 400)
        
        return JsonResponse({"message" : "SUCCESS"}, status = 201)