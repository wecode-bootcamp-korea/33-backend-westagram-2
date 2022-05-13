import json

from django.views import View
from django.http import JsonResponse

from .models import Accounts


class SignupView(View):
    def post(self, request):
        
        try :
            signup_data = json.loads(request.body)
        
            if "@" not in signup_data["email"] or "." not in signup_data["email"] :
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 400)

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