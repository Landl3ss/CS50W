from nis import cat
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments


def index(request):
    listings = Listings.objects.all().filter(active=True)
    # print(listings)
    return render(request, "auctions/index.html", {
        'listings': listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create_listing(request):

    if request.method == "POST":
        item = request.POST['item']
        starting_price = float(request.POST['starting_price'])
        image_url = request.POST['image_url']
        desc = request.POST['description']
        category = request.POST['category']
        listing = Listings(seller=User.objects.get(username=request.user), item=item, description=desc, starting_price=starting_price, current_price=starting_price, image=image_url, category=category)
        listing.save()
        # print(listing.seller)
        # print(listing.active)
        # print(listing.starting_price)
        # print(listing.item)
        l = Listings.objects.get(seller=User.objects.get(username=request.user), item=item, description=desc, starting_price=starting_price, current_price=starting_price, image=image_url)
        return HttpResponseRedirect(reverse("listing", kwargs={'pk': l.pk}))

    return render(request, "auctions/create_listing.html")


@login_required(login_url='login')
def listing(request, pk):
    user = User.objects.get(username=request.user)
    listing = Listings.objects.get(pk=pk)

    if listing.active == False:
        unwatch = False
        you_won = False
        winner = Bids.objects.get(pk=pk, amount=listing.current_price)
        if winner.bidder == user:
            you_won = True
        if listing in user.watchlist:
            unwatch = True
        return render(request, "auctions/closed_listing.html", {
        'listing' : listing,
        'comments' : comments,
        'you_won' : you_won,
        'unwatch' : unwatch
    })
        
    if request.method == 'POST':
        if 'price' in request.POST:
            price = request.POST['price']
            listing.update(current_price=price)
            listing.save()
            bid = Bids(bidder=user, amount=price, item=listing)
            bid.save()
        
        if 'comment' in request.POST:
            comment = request.POST['comment']
            co = Comments(commenter=user, comment=comment, item=listing)
            co.save()
    
    watchlist = True
    unwatchable = False
    comments = Comments.objects.filter(item=listing).order_by("-pk")
    if request.user == listing.seller:
        watchlist = False
    if listing in user.watchlist:
        unwatchable = True

    min_price = listing.current_price + 1
    return render(request, "auctions/listing.html", {
        'listing' : listing,
        'comments' : comments,
        'watchlist' : watchlist,
        'unwatchable' : unwatchable,
        'min_price' : min_price
    })


@login_required(login_url='login')
def wl(request, pk):
    user = User.objects.get(username=request.user)
    listing = Listings.objects.get(pk=pk) 
    if listing in user.watchlist:
        user.watchlist.remove(listing)
    else:
        user.watchlist.append(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk})) 


@login_required(login_url='login')
def watchlist(request):
    user = User.objects.get(username=request.user)
    return render(request, 'auctions/watchlist.html', {
        'watchlist' : user.watchlist
    })


@login_required(login_url='login')
def categories(request):
    obj = Listings.object.all().filter(active=True)
    categories = []
    for i in obj:
        if i.category not in categories:
            categories.append(i.category)
    return render(request, 'auctions/categories.html', {
        'categories' : categories
    })


@login_required(login_url='login')
def category(request, categ):
    links = Listings.objects.all().filter(active=True, category=categ)
    return render(request, 'auctions/category.html', {
        'links' : links,
        'categ' : categ
    })


@login_required(login_url='login')
def closed(request, pk):
    act = Listings.objects.get(pk=pk)
    act.active = False
    act.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk})) 