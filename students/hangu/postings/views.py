import json

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from .models import Posting, Comment
from users.utils import token_reader

class PostingView(View):
    @token_reader
    def post(self, request):
        try:
            post_data = json.loads(request.body)

            title        = post_data["title"]
            content      = post_data["content"]
            image_url    = post_data["image_url"]
            user         = request.user
            
            posting = Posting(
                title     = title,
                content   = content,
                image_url = image_url,
                user_id   = user.id
                )
            posting.save()

            return JsonResponse({"message":"POSTING이 정상적으로 저장되었습니다"}, status=200)
        except TypeError:
            return JsonResponse({"message": 'TypeError'}, status=401)
    
    @token_reader
    def get(self, request):
        postings = Posting.objects.filter(user_id = request.user.id)
        posting_list = [{
                    'user_id'            : posting.user.id,
                    'user_name'          : posting.user.user_name,
                    'posting_id'         : posting.id,
                    'posting_title'      : posting.title,
                    'posting_content'    : posting.content,
                    'posting_image_url'  : posting.image_url,
                    'posting_create_time': posting.created_at,
                } for posting in postings]
        
        return JsonResponse({
                'posting': posting_list,
                'message': 'SUCCESS',
                }, status=200)


class CommentsView(View):
    @token_reader
    def post(self, request):
        comment = json.loads(request.body)
        
        content = comment['user_content']
        user_id = request.user.id
        posting_id = comment['posting_id']
        created_at = comment["created_at"]

        comments = Comment(
            content    = content,
            user_id    = user_id,
            posting_id = posting_id,
            created_at = created_at
            )
        comments.save()

        return JsonResponse({'message':'정상적으로 저장되었습니다'}, status = 200)    



