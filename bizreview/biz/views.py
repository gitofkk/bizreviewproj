from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.http import Http404
from django.urls import reverse
from dal import autocomplete
from cities.models import Country, Region
from .forms import AddressForm, UserForm, ComplaintForm
from .models import Complaint, Address


# Create your views here.
def home(request):
    address_form = AddressForm(request.POST or None)
    del address_form.fields['region']
    del address_form.fields['country']

    if address_form.is_valid():
        # field__unaccent__lower__trigram_similar
        kargs = {
            'flat_no__icontains': address_form.cleaned_data['flat_no'],
            'building_name__icontains': address_form.cleaned_data['building_name'],
            'street__icontains': address_form.cleaned_data['street'],
            'area__icontains': address_form.cleaned_data['area'],
            'city__icontains': address_form.cleaned_data['city'],
            'postcode__icontains': address_form.cleaned_data['postcode']
        }
        records = Address.objects.filter(**kargs).values()
        return render(request, 'biz/search_result.html', {'records': records})

    return render(request, 'biz/home.html', {'address_form': address_form})


def show_post(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, is_active=False)

    user_form = UserForm(instance=complaint.user)
    del user_form.fields['email']

    address_form = AddressForm(instance=complaint.address)
    address_form.fields['region'].help_text = address_form.instance.region.name
    address_form.fields['country'].help_text = address_form.instance.country.name

    complaint_form = ComplaintForm(instance=complaint)
    del complaint_form.fields['agree']

    context = {
        'address_form': address_form,
        'review_list': zip(complaint_form, user_form),
        'published_date': complaint_form.instance.published_date
    }
    return render(request, 'biz/show_post.html', context)


def add_post(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        complaint_form = ComplaintForm(request.POST)

        if user_form.is_valid() and address_form.is_valid() and complaint_form.is_valid():
            user = user_form.save(commit=False)
            address = address_form.save(commit=False)
            complaint = complaint_form.save(commit=False)
            user.save()
            address.save()

            complaint.user = user
            complaint.address = address
            complaint.verify_code = get_random_string(length=32)
            complaint.save()

            return redirect('post_success', pk=complaint.pk)
    else:
        user_form = UserForm()
        address_form = AddressForm()
        complaint_form = ComplaintForm()
    return render(request, 'biz/add_post.html', {'user_form': user_form, 'address_form': address_form, 'complaint_form': complaint_form})


def post_success(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    subject = 'Activation link to publish your post'
    message = 'Dear ' + complaint.user.name
    message += 'Click the below link to publish your post.'
    message += reverse('post_publish', args=(pk, complaint.verify_code))
    message += 'Thank you!'
    sender = settings.EMAIL_HOST_USER
    receiver = (complaint.user.email, )
    send_mail(subject, message, sender, receiver, fail_silently=False)
    return render(request, 'biz/post_success.html', {'complaint': complaint})


def post_publish(request, pk, code):
    complaint = get_object_or_404(Complaint, pk=pk)
    if code != complaint.verify_code:
        raise Http404
    complaint.is_active = True
    complaint.save()
    # Send email with delete post link
    subject = 'Link to delete your post'
    message = 'Dear ' + complaint.user.name
    message += 'Click the below link to delete your post in future.'
    message += reverse('post_delete', args=(pk, complaint.verify_code))
    message += 'Thank you!'
    sender = settings.EMAIL_HOST_USER
    receiver = (complaint.user.email, )
    send_mail(subject, message, sender, receiver, fail_silently=False)
    return render(request, 'biz/post_publish.html', {})

def post_delete(request, pk, code):
    complaint = get_object_or_404(Complaint, pk=pk)
    if code != complaint.verify_code:
        raise Http404
    Complaint.objects.filter(pk=pk).delete()
    return render(request, 'biz/post_delete.html', {})

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class RegionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Region.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs