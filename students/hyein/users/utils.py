import json, jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user = User.objects.get(id = payload['id'])
            request.user = user      
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'Message': 'Invalid Token'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'Message': 'Invalid User'}, status=401)
        
        return func(self,request,*args, **kwargs)
    
    return wrapper