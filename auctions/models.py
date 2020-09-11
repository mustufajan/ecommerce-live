from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files import File

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):

    category_choices = [
        ('Home & Electronics', 'Home & Electronics'),
        ('Fashion', 'Fashion'),
    ]

    title=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to='listing_images')
    creation_date_time=models.DateTimeField(auto_now_add=True)
    seller=models.ForeignKey('User', on_delete=models.CASCADE, related_name="listings")
    active=models.BooleanField(default=True)
    category=models.CharField(
        max_length= 20,
        choices= category_choices,
        default= 'FASHION')

    def __str__(self):
        return f"{self.title.capitalize()} for ${self.price}"

class Bid(models.Model):
    value=models.DecimalField(max_digits=10, decimal_places=2)
    bidder=models.ForeignKey('User', on_delete=models.CASCADE, related_name="submitted_bids_user")
    bidding_date_time=models.DateTimeField(auto_now_add=True)
    listing=models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="submitted_bids_listing")

    def __str__(self):
        return f"{self.bidder} bid ${self.value} on ({self.listing})"

class Comment(models.Model):
    text=models.TextField(max_length=500)
    listing=models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="comments")
    commenter=models.ForeignKey('User', on_delete=models.CASCADE)
    creation_date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

class Watchlist(models.Model):
    listing=models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="watchlist_listing")
    watcher=models.ForeignKey('User', on_delete=models.CASCADE, related_name="watchlist_user")
    creation_date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"\"{self.listing}\" watched by {self.watcher}"


