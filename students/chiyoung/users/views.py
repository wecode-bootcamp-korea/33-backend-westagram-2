import json

from django.views import View
from django.http import JsonResponse

from .models import Accounts


class SignupView(View):
    def post(self, request):
        signup_data = json.loads(request.body) # dictionary type
        
        try :
            if Accounts.objects.filter(email=signup_data["email"]).exists():
                return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except :
            account = Accounts.objects.create(
            name         = signup_data["name"],
            email        = signup_data["email"],
            password     = signup_data["password"],
            phone_number = signup_data["phone_number"],
            created_at   = signup_data["created_at"],
            updated_at   = signup_data["updated_at"]
        )
        
        return JsonResponse({"message" : "SUCCESS"}, status = 201)