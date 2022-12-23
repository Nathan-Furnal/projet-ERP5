from django import forms


class OfferForm(forms.Form):
    partner_name = forms.CharField(label="Buyer", max_length=200)
    offer_amt = forms.IntegerField(label="Amount")
    apart_id = forms.IntegerField(label="Apartment")

