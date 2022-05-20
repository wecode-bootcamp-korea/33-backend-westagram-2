import json

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from .models import Like, Posting, Comment
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
    def post(self, request, posting_id):
        try:
            comment_data = json.loads(request.body)
            
            content    = comment_data["content"]

            comments = Comment(
                content    = content,
                user_id    = request.user.id,
                posting_id = posting_id,
                )
            comments.save()

            return JsonResponse({'message':'comment가 정상적으로 저장되었습니다'}, status = 200)    
        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status=401)

    @token_reader
    def get(self, request, posting_id):
        try:
            comments = Comment.objects.filter(posting_id = posting_id)

            if not comments:
                return JsonResponse({'message':'댓글이 없습니다'}, status = 400)

            comment_list = [{
                        '댓글 작성자 id': comment.user.id,
                        '댓글 작성자 이름': comment.user.user_name,
                        '댓글 내용'    : comment.content,
                        '댓글 작성 시간' : comment.created_at,
                    } for comment in comments]

            return JsonResponse({'message':'SUCCESS', 'comments':comment_list}, status = 200)
        except KeyError:
            return JsonResponse({"message": 'KeyError'}, status=401)


class LikeCountView(View):
    @token_reader
    def post(self, request, posting_id):
        like_users = Like.objects.filter(posting_id=posting_id, like_user_id = request.user.id)
        if not like_users.exists():
            likes = Like(
                like_user_id = request.user.id,
                posting_id = posting_id,
            )
            likes.save()
            return JsonResponse({'message':'좋아요가 등록되었습니다'}, status = 200)
        like_user = Like.objects.get(like_user_id = request.user.id)
        like_user.delete()
        return JsonResponse({'message':'좋아요를 취소하셨습니다.'}, status = 400)   

    def get(self, request, posting_id):
        likes = Like.objects.filter(posting_id = posting_id)

        like_count= likes.count()

        return JsonResponse({'like_counting':like_count}, status=200)
