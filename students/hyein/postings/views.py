import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from postings.models import Post, Image
from users.models import User
from users.utils import login_decorator
 
class PostingView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            
            content    = data.get('content')
            image_list = data.get('image').split(',')
            
            post = Post.objects.create(
                content = content,
                user    = user,
            )
            
            for image in image_list:
                Image.objects.create(
                    image = image,
                    post  = post,
                )
            
            return JsonResponse({'MASSAGE' : 'SUCCESS'}, status = 200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=404)
        
        except KeyError: 
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)
    @login_decorator    
    def get(self, request):
        post_list = [{
            "username" : User.objects.get(id = post.user.id).name,
            "content"  : post.content,
            "images"   : [i.image for i in Image.objects.filter(post_id = post.id)],
            "create_at": post.created_at
        } for post in Post.objects.all()
        ]
        
        return JsonResponse({'DATA' :post_list}, status = 200)
    
class PostingSearchView(View):
    @login_decorator
    def get(self, request, user_id):
        if not User.objects.filter(id = user_id).exists():
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)

        post_list = [{
            "username"  : User.objects.get(id = post.user_id).name,
            "content"   : post.content,
            "image_url" : [i.image for i in Image.objects.filter(post_id = post.id)],
            "create_at" : post.created_at
            } for post in Post.objects.filter(user_id=user_id)
            ]

        return JsonResponse({'data':post_list}, status=200)