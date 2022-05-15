import json

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import Accounts
from .validators import validate_email, validate_password

class SignupView(View):
    def post(self, request):

        try :
            signup_data = json.loads(request.body)

            email        = signup_data["email"]
            password     = signup_data["password"]

            if not validate_email(email) :
                raise ValidationError("INVALID_EMAIL")

            if not validate_password(password) :
                raise ValidationError("INVALID_PASSWORD")
            
            if Accounts.objects.filter(email=email).exists() :
                raise ValidationError("EMAIL_ALREADY_EXIST")

            Accounts.objects.create(
                name         = signup_data["name"],
                email        = email,
                password     = password,
                phone_number = signup_data["phone_number"]
            )

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"MESSAGE": "REQUEST_WITHOUT_DATA"}, status=400)

        except KeyError :
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValidationError as verr :
            return JsonResponse({"MESSAGE": verr.message}, status=400)