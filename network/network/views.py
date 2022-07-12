from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Like, Follows

import json


def index(request):

    user = str(request.user)
    postslist = []
    post = Post.objects.all().order_by('-time')
    for p in post:
        if p.author.username == user:
            postslist.append(p.serialize(True))
        else:
            postslist.append(p.serialize(False))

    paginated = Paginator(postslist, 10)
    posts = paginated.page(1)
    # print(type(posts.number))
    # print(posts.next_page_number)
    return render(request,'network/index.html', {
        'posts': posts.object_list,
        'page_number': posts,
        'paginated': paginated,
        'p': posts.number,
        'previous': False,
        'next': 2
    })


def page(request, num):
    user = str(request.user)
    postslist = []
    post = Post.objects.all().order_by('-time')
    for p in post:
        if p.author.username == user:
            postslist.append(p.serialize(True))
        else:
            postslist.append(p.serialize(False))

    paginated = Paginator(postslist, 10)
    posts = paginated.page(num)

    if posts.has_next():
        next = num + 1
    else:
        next = False
    previous = num - 1
    if previous == 0:
        previous = False
    return render(request, 'network/index.html', {
        'posts': posts.object_list,
        'page_number': posts,
        'paginated': paginated,
        'p': posts.number,
        'previous': previous,
        'next': next
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):

    num = 1

    # Find the user
    try:
        user = User.objects.get(username=username) 
    except:
        return JsonResponse({"error": "User doesn't exist."}, status=404)

    post = Post.objects.all().filter(author=user).order_by("-time")

    followers = len(Follows.objects.all().filter(account=user, isfollowing=True))
    following = len(Follows.objects.all().filter(follower=user, isfollowing=True))

    # print(following)
    # print(followers)
    postslist = []
    for p in post:
        if p.author.username == user:
            postslist.append(p.serialize(True))
        else:
            postslist.append(p.serialize(False))
    paginated = Paginator(postslist, 10)
    posts = paginated.page(num)

    if request.user == user:
        same = True
    else:
        same = False
    
    if posts.has_next():
        next = num + 1
    else:
        next = False
    previous = num - 1
    if previous == 0:
        previous = False

    return render(request, "network/profile.html", {
        'user': user,
        'posts': posts,
        'following': following,
        'followers': followers,
        'same': same,
        'posts': posts.object_list,
        'page_number': posts,
        'paginated': paginated,
        'p': posts.number,
        'previous': previous,
        'next': next
    })


def profile_page(request, user, num):
    
    # Find the user
    try:
        user = User.objects.get(username=user) 
    except:
        return JsonResponse({"error": "User doesn't exist."}, status=404)

    post = Post.objects.all().filter(author=user).order_by("-time")
    following = len(user.following)
    followers = 0
    for u in User.objects.all():
        if user in u.following:
            followers += 1

    postslist = []
    for p in post:
        if p.author.username == user:
            postslist.append(p.serialize(True))
        else:
            postslist.append(p.serialize(False))
    paginated = Paginator(postslist, 10)
    posts = paginated.page(num)
    if request.user == user:
        same = True
    else:
        same = False
    
    if posts.has_next():
        next = num + 1
    else:
        next = False
    previous = num - 1
    if previous == 0:
        previous = False

    return render(request, "network/profile.html", {
        'user': user,
        'posts': posts,
        'following': following,
        'followers': followers,
        'same': same,
        'posts': posts.object_list,
        'page_number': posts,
        'paginated': paginated,
        'p': posts.number,
        'previous': previous,
        'next': next
    })


def post_entry(request, sendto):

    # print(request.POST)
    if request.method == "POST":
        # text = json.loads(request.body)
        text = request.POST['speech']
        
        # print(text['speech'])
        complete = Post(author=request.user, text=text)
        complete.save()

        if sendto == "profile":
            return HttpResponseRedirect(reverse(sendto, kwargs={'username': request.user}))

        return HttpResponseRedirect(reverse(sendto))
    
    else:
        return JsonResponse({"error": "POST request required"}, status=400)


@csrf_exempt
def edit_post(request, postid):

    if request.method == "PUT":
        
        try:
            post_in_q = Post.objects.get(pk=postid)
        except:
            return JsonResponse({"error": "Post doesn't exist."}, status=404)
        
        text = json.loads(request.body)
        post_in_q.text = text['speech']
        post_in_q.save()

        return JsonResponse({"message": "Successful edit of post."}, status=201)

    else:
        return JsonResponse({"error": "PUT request required"}, status=400)


@csrf_exempt
def likeit(request, postid):

    p = Post.objects.get(pk=postid)
    like_count = Like.objects.all().filter(the_post=p, liked=True)
    
    if not request.user.is_authenticated:
        return JsonResponse({'exist': False, 'likes': len(like_count)})

    u = User.objects.get(username=request.user)
     
    if request.method == 'GET':

        try:
            l = Like.objects.get(the_post=p, liker=u)
        except:
            q = Like(the_post=p, liker=u)
            q.save()
            return JsonResponse({'like': False, 'exist': True, 'likes': len(like_count)}, status=200)
        
        if l.liked == False:
            # print(l)
            return JsonResponse({'like': False, 'exist': True, 'likes': len(like_count)}, status=200)
        else:
            return JsonResponse({'like': True, 'exist': True, 'likes': len(like_count)}, status=200)

    if request.method == 'PUT':

        data = json.loads(request.body)
        l = Like.objects.get(the_post=p, liker=u)
        l.liked = data['like']
        l.save()
        return HttpResponse(status=204)

    return JsonResponse({'error': "GET or PUT is required."}, status=400)


def following(request):

    user = User.objects.all().filter(username=request.user)

    following = Follows.objects.all().filter(follower=user[0], isfollowing=True)
    f = []
    for i in following:
        f.append(i.account)
    
    following_posts = Post.objects.all().filter(author__in=f).order_by("-time")


    paginated = Paginator(following_posts, 10)
    fp = paginated.page(1)
    return render(request, "network/following.html", {
        'following_posts': fp.object_list,
        'previous': False,
        'next': 2,
        'page_number': fp,
        'paginated': paginated,
        'p': fp.number
    })
    


def following_page(request, num):
    user = User.objects.all().filter(username=request.user)

    following = Follows.objects.all().filter(follower=user[0], isfollowing=True)
    f = []
    for i in following:
        f.append(i.account)
    
    following_posts = Post.objects.all().filter(author__in=f).order_by("-time")


    paginated = Paginator(following_posts, 10)
    fp = paginated.page(num)

    if fp.has_next():
        next = num + 1
    else:
        next = False
    previous = num - 1
    if previous == 0:
        previous = False
    return render(request, 'network/following.html', {
        'following_posts': fp.object_list,
        'page_number': fp,
        'paginated': paginated,
        'p': fp.number,
        'previous': previous,
        'next': next
    })


@csrf_exempt
def to_follow(request, following):

    follower = User.objects.get(username=request.user)
    account = User.objects.get(username=following)
    
    if request.method == "GET":
        try:
            f = Follows.objects.get(account=account, follower=follower)
        except:
            f = Follows(account=account, follower=follower, isfollowing=False)
            f.save()
            return JsonResponse({'following': False}, status=200)

        return JsonResponse({'following': True}, status=200)

    if request.method == "PUT":
        torf = json.loads(request.body)
        if torf['follow'] == True:
            new = Follows.objects.get(account=account, follower=follower)
            new.isfollowing = True
            new.save()
        else:
            new = Follows.objects.get(account=account, follower=follower)
            new.isfollowing = False
            new.save()

        return JsonResponse({'message': "Successfully changed."}, status=200)
