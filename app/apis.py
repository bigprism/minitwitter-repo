from django.http import JsonResponse

from .models import Post

from .models import Post, Like

from .models import Post, Comment

from .models import User


def post_list_api(request):
    posts = Post.objects.all().order_by('-created_at')
    data = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for post in posts
    ]
    return JsonResponse(data, safe=False)


def post_detail_api(request, pk):
    post = Post.objects.get(pk=pk)
    data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return JsonResponse(data)


def post_create_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.create(
            title=data['title'],
            content=data['content'],
            author=request.user,
        )
        return JsonResponse({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def post_delete_api(request, pk):
    if request.method == 'DELETE':
        post = Post.objects.get(pk=pk)
        post.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def post_like_api(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        like = Like.objects.create(
            post=post,
            user=request.user,
        )
        return JsonResponse({
            'id': like.id,
            'post': like.post.id,
            'user': like.user.username,
            'created_at': like.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def post_comment_api(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=data['content'],
        )
        return JsonResponse({
            'id': comment.id,
            'post': comment.post.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def user_profile_api(request, username):
    user = User.objects.get(username=username)
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile_picture': user.profile_picture.url,
        'bio': user.bio,
        'following': [user.id for user in user.following.all()],
        'followers': [user.id for user in user.followers.all()],
        'posts': [post.id for post in user.posts.all()],
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return JsonResponse(data)


def user_follow_api(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        request.user.following.add(user)
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def user_unfollow_api(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        request.user.following.remove(user)
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({'error': 'Invalid request method.'})