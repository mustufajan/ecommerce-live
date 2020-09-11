from django import forms
from .models import *

class ListingForm(forms.Form):
    title=forms.CharField(label= 'Name',max_length=64)
    price=forms.DecimalField(label='Lowest bid', max_digits=10, decimal_places=2)
    description=forms.CharField(label='Describe your listing', widget=forms.Textarea)
    image=forms.FileField()
    category= forms.CharField(label='Category', widget=forms.Select(choices=Listing.category_choices))


class BidForm(forms.Form):
    bid_value=forms.DecimalField(label='', max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder':'$ Enter bid value here'}))


    
    


