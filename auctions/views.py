from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Max




def index(request):
    return render(request, "auctions/index.html",{
        'listings':Listing.objects.filter(active=True)
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

@login_required
def create_listing(request):
    if request.method == 'POST':
        form=ListingForm(request.POST, request.FILES)
        if form.is_valid():

            l = Listing(title=form.cleaned_data['title'], 
                        price=form.cleaned_data['price'], 
                        description=form.cleaned_data['description'], 
                        image=form.cleaned_data['image'], 
                        seller=request.user)
            l.save()
            
            return HttpResponseRedirect(reverse("listing", args=(l.id,)))
        else:
            return HttpResponse(f'{form.errors}')

    else:
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            'form':form
        })

@login_required
def listing(request, listing_id):

    listing = Listing.objects.filter(id=listing_id).first()
    watched= listing.watchlist_listing.filter(watcher=request.user).first()
    user_bid= listing.submitted_bids_listing.filter(bidder=request.user).last()
    number_of_bids = Bid.objects.filter(listing=listing).count()
    bid_form = BidForm()
    max_bid = 0
    max_bidder = listing.seller

    if number_of_bids > 0:
        max_bid = Bid.objects.filter(listing=listing).aggregate(Max('value'))
        max_bidder = Bid.objects.filter(value=max_bid['value__max']).first
   

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'watched': watched,
        'bid_form': bid_form,
        'user_bid': user_bid,
        'number_of_bids': number_of_bids,
        'max_bid': max_bid,
        'max_bidder': max_bidder,
        'comments': Comment.objects.filter(listing=listing)
    })

@login_required
def watchlist(request, listing_id):

    listing = Listing.objects.filter(id=listing_id).first()
    w = Watchlist.objects.filter(watcher=request.user, listing=listing)
    
    if not w :
        print("added!")
        add = Watchlist(listing=listing, watcher=request.user)
        add.save()
        print(w)
    else:
        print("deleted!")
        w.delete()
     
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def bid(request, listing_id):

    form=BidForm(request.POST, request.FILES)
    
    listing = Listing.objects.filter(id=listing_id).first()
    user_bid = Bid.objects.filter(listing=listing, bidder=request.user).last()
    number_of_bids = Bid.objects.filter(listing=listing).count()

    if number_of_bids > 0:
        max_bid = Bid.objects.filter(listing=listing).aggregate(Max('value'))
        max_bidder = Bid.objects.filter(value=max_bid['value__max']).first

    if user_bid and max_bid['value__max']==user_bid.value:
        return HttpResponse(f'You have already submitted a bid for this item')

    elif form.is_valid():

        bid_value=form.cleaned_data['bid_value']
        if number_of_bids > 0:
            max_bid = Bid.objects.all().aggregate(Max('value'))
            print(f'{max_bid}')

            if bid_value >=  listing.price and bid_value >  max_bid['value__max']:
                if user_bid:
                    user_bid=Bid(value=bid_value, listing=listing, bidder=request.user)
                    user_bid.save()
                else:
                    new_bid = Bid(value=bid_value, listing=listing, bidder=request.user)
                    new_bid.save()
                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse(f'You must submit a bid higher than the current highest bidder')
        else:
            if bid_value >=  listing.price:
                new_bid = Bid(value=bid_value, listing=listing, bidder=request.user)
                new_bid.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse(f'You must submit a bid higher than the listing price')

    else:
        return HttpResponse(f'{form.errors}')
      

@login_required
def listing_status(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if listing.active:
        listing.active = False
        
    else:
        listing.active = True

    listing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def my_listings(request):
    return render(request, "auctions/my_listings.html", {
        'my_listings': Listing.objects.filter(seller=request.user)
    })

@login_required
def my_bids(request):
    return render(request, "auctions/my_bids.html", {
        'my_bids': Bid.objects.filter(bidder=request.user)
    })

@login_required
def comment(request, listing_id):
    l = Comment(text=request.POST['comment'], commenter=request.user, listing= Listing.objects.filter(id=listing_id).first())
    l.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def my_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'watchlist': Watchlist.objects.filter(watcher=request.user)
    })

@login_required
def categories(request):

    categories = Listing.objects.order_by('category').values('category').distinct()
    return render(request, "auctions/categories.html",{
        'categories': categories  
    })

@login_required
def categorized_listings(request, category):

    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/categorized_listings.html", {
        'listings': listings
    })
