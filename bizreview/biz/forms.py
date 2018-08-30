from django import forms
from dal import autocomplete
from .models import User, Address, Complaint

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'name': 'Your name',
            'email': 'Your Email Address'
        }


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'flat_no': 'Door / Flat No',
            'building_name': 'Building / Apartment Name',
            'street': 'Street (Address Line 1)',
            'area': 'Area (Address Line 2)',
            'city': 'Town / City',
            'postcode': 'Postal / Zip Code',
            'region': 'State / Province'
        }
        widgets = {
            'region': autocomplete.ModelSelect2(url='region-autocomplete'),
            'country': autocomplete.ModelSelect2(url='country-autocomplete')
        }


class ComplaintForm(forms.ModelForm):
    agree = forms.BooleanField(required=True, help_text='I agree to the terms and conditions.', label=False)

    class Meta:
        model = Complaint
        fields = ('comment', )
        labels = {
            'comment': 'Comments'
        }
